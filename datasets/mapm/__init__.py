import os
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter
from sklearn import model_selection
from sklearn.model_selection import KFold


sensors = ["volt", "rotate", "pressure", "vibration"]


def load_data():
    fp = os.path.dirname(__file__)

    # Sensor data
    data = pd.read_csv(fp + "/PdM_telemetry.csv.gz")

    # Error alarm logs
    data = data.merge(
        pd.read_csv(fp + "/PdM_errors.csv.gz"), how="left", on=["datetime", "machineID"]
    )

    # Failure logs
    data = data.merge(
        pd.read_csv(fp + "/PdM_failures.csv.gz"),
        how="left",
        on=["datetime", "machineID"],
    )

    # Formatting
    data.datetime = pd.to_datetime(data.datetime)

    return data


def cleaning(df):
    # NaN values are encoded to -1
    df = df.sort_values("errorID")
    df.errorID = df.errorID.factorize()[0]
    df = df.sort_values("failure")
    df.failure = df.failure.factorize()[0]
    df = df.sort_values(["machineID", "datetime"])

    df.errorID = df.errorID.astype("int")
    df.failure = df.failure.astype("int")

    df.volt = df.volt.astype("float32")
    df.rotate = df.rotate.astype("float32")
    df.pressure = df.pressure.astype("float32")
    df.vibration = df.vibration.astype("float32")

    df.datetime = pd.to_datetime(df.datetime)
    return df


def load_clean_data():
    return cleaning(load_data())


def generate_run_to_failure(
    raw_data,
    health_censor_aug=1000,
    min_lifetime=10,
    max_lifetime=300,
    seed=123,
    outfn=None,
):
    run_to_failure = []
    error_ids = raw_data.errorID.dropna().sort_values().unique().tolist()

    for machine_id, g in tqdm.tqdm(
        raw_data.groupby("machineID"), desc="run-to-failure"
    ):
        g = g.set_index("datetime").sort_index()

        start_date = g.index.values[0]
        failures = g.loc[~g.failure.isnull()]

        for event_time, event in failures.iterrows():
            # Extracting a single cycle/process
            cycle = g[start_date:event_time].drop("machineID", axis=1)

            lifetime = (event_time - start_date).days
            if lifetime < 1:
                start_date = event_time
                continue

            numerical_features = (
                cycle.agg(["min", "max", "mean"]).unstack().reset_index()
            )
            numerical_features["feature"] = numerical_features.level_0.str.cat(
                numerical_features.level_1, sep="_"
            )
            numerical_features = numerical_features.pivot_table(
                columns="feature", values=0
            )

            categorical_features = pd.DataFrame(
                Counter(cycle.errorID), columns=error_ids, index=[0]
            )

            sample = pd.concat([numerical_features, categorical_features], axis=1)
            sample[["machine_id", "lifetime", "broken"]] = machine_id, lifetime, 1

            run_to_failure.append(sample)
            start_date = event_time

    run_to_failure = pd.concat(run_to_failure, axis=0).reset_index(drop=True)

    health_censors = censoring_augmentation(
        raw_data,
        n_samples=health_censor_aug,
        min_lifetime=min_lifetime,
        max_lifetime=max_lifetime,
        seed=seed,
    )

    run_to_failure = pd.concat([run_to_failure, health_censors])

    # Shuffle
    run_to_failure = run_to_failure.sample(frac=1, random_state=seed).reset_index(
        drop=True
    )
    run_to_failure = run_to_failure.fillna(0.0)

    if outfn is not None:
        run_to_failure.to_csv(outfn, index=False)

    return run_to_failure


def censoring_augmentation(
    raw_data, n_samples=10, max_lifetime=150, min_lifetime=2, seed=123
):
    error_ids = raw_data.errorID.dropna().sort_values().unique().tolist()
    np.random.seed(seed)
    samples = []
    pbar = tqdm.tqdm(total=n_samples, desc="augmentation")

    while len(samples) < n_samples:
        censor_timing = np.random.randint(min_lifetime, max_lifetime)
        machine_id = np.random.randint(100) + 1
        tmp = raw_data[raw_data.machineID == machine_id]
        tmp = tmp.drop("machineID", axis=1).set_index("datetime").sort_index()

        failures = tmp[~tmp.failure.isnull()]
        if failures.shape[0] < 2:
            continue

        failure_id = np.random.randint(failures.shape[0])
        failure = failures.iloc[failure_id]
        event_time = failure.name
        start_date = (
            tmp.index.values[0]
            if failure_id == 0
            else failures.iloc[failure_id - 1].name
        )

        # censoring
        cycle = tmp[start_date:event_time]
        cycle = cycle.iloc[:censor_timing]

        if not cycle.shape[0] == censor_timing:
            continue

        numerical_features = (
            cycle.agg(["min", "max", "mean", "std"]).unstack().reset_index()
        )
        numerical_features["feature"] = numerical_features.level_0.str.cat(
            numerical_features.level_1, sep="_"
        )
        numerical_features = numerical_features.pivot_table(columns="feature", values=0)

        categorical_features = pd.DataFrame(
            Counter(cycle.errorID), columns=error_ids, index=[0]
        )

        sample = pd.concat([numerical_features, categorical_features], axis=1)
        sample[["machine_id", "lifetime", "broken"]] = machine_id, censor_timing, 0
        samples.append(sample)
        pbar.update(1)

    pbar.close()
    return pd.concat(samples).reset_index(drop=True).fillna(0)


def generate_validation_sets(method="kfold", n_splits=5, seed=123, outdir=None):
    validation_sets = []

    if method == "kfold":
        # K-fold cross validation
        assert type(n_splits) == int
        assert n_splits > 2

        raw_data = load_data()

        kfold = model_selection.KFold(
            n_splits=n_splits, shuffle=True, random_state=seed
        )
        for i, (train_index, test_index) in enumerate(kfold.split(np.arange(100))):
            print("K-fold {}/{}".format(i + 1, n_splits))
            # train/test split by machine ID
            train_machines = raw_data[raw_data.machineID.isin(train_index)]
            test_machines = raw_data[raw_data.machineID.isin(test_index)]
            # print('train:', train_machines.shape)
            # print('test:', test_machines.shape)

            # convert the two sets into run-to-failure data
            train_censored_data = generate_run_to_failure(
                train_machines, health_censor_aug=len(train_index) * 10, seed=seed
            )
            test_consored_data = generate_run_to_failure(
                test_machines, health_censor_aug=len(test_index) * 10, seed=seed
            )

            # print('train:', train_censored_data.shape)
            # print('test:', test_consored_data.shape)

            validation_sets.append((train_censored_data, test_consored_data))

            if outdir is not None:
                train_censored_data.to_csv(outdir + f"/train_{i}.csv.gz", index=False)
                test_consored_data.to_csv(outdir + f"/test_{i}.csv.gz", index=False)

    elif method == "leave-one-out":
        raise NotImplementedError

    return validation_sets


def load_validation_sets(filepath, n_splits=5):
    return [
        (
            pd.read_csv(filepath + f"/train_{i}.csv.gz"),
            pd.read_csv(filepath + f"/test_{i}.csv.gz"),
        )
        for i in range(n_splits)
    ]


def plot_sequence_and_events(data, machine_id=1):
    data = data[data.machineID == machine_id]
    fig, ax = plt.subplots(4 + 2, figsize=(8, 8))

    data.plot(y="volt", legend=True, ax=ax[0])
    data.plot(y="rotate", legend=True, ax=ax[1])
    data.plot(y="pressure", legend=True, ax=ax[2])
    data.plot(y="vibration", legend=True, ax=ax[3])

    if data.errorID.isnull().sum() < data.errorID.shape[0]:
        pd.get_dummies(data.errorID).plot(ax=ax[4])
    if data.failure.isnull().sum() < data.failure.shape[0]:
        pd.get_dummies(data.failure).plot(ax=ax[5])

    ax[0].set_title("Machine #{}".format(machine_id))

    for i in range(5):
        ax[i].set_xlabel(None)
        ax[i].set_xticklabels([])

    fig.tight_layout()

    return fig, ax


def gen_summary(outdir=None):
    if outdir is None:
        outdir = os.path.dirname(__file__)

    os.makedirs(outdir, exist_ok=True)
    df = load_data()

    with PdfPages(outdir + "/mapm_summary.pdf") as pp:
        for i in tqdm.trange(1, 101):
            fig, _ = plot_sequence_and_events(df, machine_id=i)
            fig.savefig(pp, format="pdf")
            plt.clf()
            plt.close()


def load_failure_sequences_list(dim=sensors,once_per_machine=False,len_thre=0):
    """

    Returns
    -------
    run-to-failure sequences  [# of seq, [dim, time]]
    failure labels  [# of seq]
    """

    clean_df = load_clean_data()
    sequence_df_list = []
    failure_list = []

    # source_df = pd.DataFrame(colums=["seq_id","machine_id"])

    clean_df["seq_id"] = 0
    for machine_id, m_df in tqdm(
        clean_df.groupby("machineID"), desc="Segment each machine data"
    ):
        # sort
        m_df = m_df.sort_values("datetime")

        # segment & set seq_id
        failures_index = m_df["failure"][m_df["failure"] > -1].index
        failures_values = m_df["failure"][m_df["failure"] > -1].values

        for ind in failures_index:
            m_df.loc[ind:, "seq_id"] += 1

        for (seq_id, seq_df), f_val in zip(m_df.groupby("seq_id"), failures_values):
            if once_per_machine:
                if len(seq_df) > len_thre:
                    sequence_df_list.append(
                        seq_df.sort_values("datetime").reset_index(drop=True).loc[:, ["machineID"]+dim]
                    )
                    failure_list.append(f_val)
                    break
                else:
                    continue
    
            else:
                sequence_df_list.append(
                    seq_df.sort_values("datetime").reset_index(drop=True).loc[:, ["machineID"]+dim]
                )
                failure_list.append(f_val)

    return sequence_df_list, failure_list


def load_clean_data_rul_k_folds(
    split_ind,
    k=5,
    random_state=0,
    once_per_machine_min=0,
):
    if once_per_machine_min==0:
        df_list = add_rul(*refine_data(*load_failure_sequences_list()))
    else:
        df_list = add_rul(*refine_data(*load_failure_sequences_list(once_per_machine=True,len_thre=once_per_machine_min)))

    data_index = range(len(df_list))

    kf = KFold(
        n_splits=k,
        random_state=random_state,
        shuffle=True,
    )

    train_idx, test_idx = list(kf.split(data_index))[split_ind]

    train_df_list = [df_list[i] for i in train_idx]
    test_df_list = [df_list[i] for i in test_idx]

    return train_df_list, test_df_list


def refine_data(sequence_df_list, failure_list, event_type="only", min_len=100):
    """
    refine_event: This data contain some sequences with complex/mulitple failue
    if "only",
    use sequences with only a failue, remove sequences with mulitple failue
    elif "all"
    use all sequences, and regard complex failues as a new types of failure
    """

    num_seq = len(failure_list)
    length_arr = np.array([len(ss) for ss in sequence_df_list])
    complex_ind = np.arange(num_seq)[length_arr <= 1]

    # whether all complex failues contains two types of failues or not
    assert not np.sum(
        np.diff(complex_ind) < 2
    ), "complex failue events contain three or more failues"

    # remove complex_ind
    apply_arr = length_arr > 1

    if event_type == "only":
        # remove complex_ind-1
        for c_id in complex_ind:
            apply_arr[c_id - 1] = False

    elif event_type == "all":
        NotImplementedError
        # check combination and define new type failures
        # complex_val = np.array(failure_list)[complex_ind]

        # # set new failure
        # for c_id,n_f in zip(complex_ind,new_failures):
        #     failure_list[c_id-1] = n_f
    else:
        NotImplementedError

    # remove sequences that not contain min_len values
    apply_length_arr = length_arr > min_len
    apply_arr &= apply_length_arr

    refined_sequence_df_list = []
    refined_failure_list = []
    for a, seq, failure in zip(apply_arr, sequence_df_list, failure_list):
        if a:
            refined_sequence_df_list.append(seq)
            refined_failure_list.append(failure)

    return refined_sequence_df_list, refined_failure_list


def add_rul(sequence_df_list, failure_list):
    label_name = "RUL"
    class_label_name = "Class"
    #
    df_list = []
    for seq_df, class_label in zip(sequence_df_list, failure_list):
        seq_df[class_label_name] = class_label
        rul_array = np.arange(len(seq_df))[::-1]
        seq_df[label_name] = rul_array
        df_list.append(seq_df)

    return df_list
