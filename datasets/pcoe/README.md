# NASA Prognostics Data Repository

The **NASA Prognostics Data Repository** is a collection of data sets donated by universities, agencies, and companies. It focuses exclusively on **prognostic data sets**, i.e., data sets that can be used for the development of prognostic algorithms. Most data sets are time-series data covering a prior nominal state to a failed state. The repository is an ongoing effort to provide valuable resources for prognostic studies.

> **Note:** This repository is also mirrored on the [Prognostics Health Management (PHM) Society website](https://data.phmsociety.org/nasa/).

---

## Usage Guidelines

- **Acknowledgment**: Publications using data from this repository must acknowledge both the repository and the data donators. This helps others access the same data sets and ensures proper credit to contributors.
- **Disclaimer**: Users employ the data at their own risk. NASA and data donators assume no liability for its use or any derived system.
- **Feedback**: Suggestions about the repository can be sent to:
  - Chetan Kulkarni: [chetan.s.kulkarni@nasa.gov](mailto:chetan.s.kulkarni@nasa.gov)
  - Christopher Teubert: [christopher.a.teubert@nasa.gov](mailto:christopher.a.teubert@nasa.gov)

---

## Data Sets

Below is a summary of the available data sets with descriptions, download links, and citations.

### 1. Algae Raceway
**Description**: Experiments on 3 small raceways with Spirulina. Data includes algae growth, decline, and environmental parameters. 
Experiments were conducted on 3 small raceways in which spirulina was inoculated. The growth and, ultimately, decline of the algae biomass was recorded along with several environmental parameters. Experiments were conducted by the Exobiology group at NASA Ames.  
**Download**: [Link](https://data.nasa.gov/download/bs7h-ane5/application%2Fzip) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/1.+Algae+Raceway.zip)  
**Data Set Citation**: Brad Bebout, et al. (NASA Ames Research Center)

---

### 2. Carbon Fiber-Reinforced Polymer (CFRP) Composites
**Description**: Run-to-failure experiments on CFRP panels, monitored using Lamb waves, strain gauges, and x-rays.
Run-to-failure experiments on CFRP panels with periodic measurements to capture internal damage growth under tension-tension fatigue. Monitoring data consists of lamb wave signals from a network of 16 piezoelectric (lead zirconate titanate – PZT) sensors and multiple triaxial strain gages. Additionally, periodic x-rays were taken to characterize internal damage as ground truth information. Three different layups were tested. Experiments were conducted at Stanford Structures and Composites Laboratory (SACL) in collaboration with the NASA Ames Research Center Prognostic Center of Excellence (PCoE). 
**Download**: [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/2.+Composites.zip)  
**Data Set Citation**: Abhinav Saxena, et al. (NASA Ames Research Center)

---

### 3. Milling
**Description**: Experiments on milling machines with varied parameters to record tool wear. 
Experiments on a milling machine for different speeds, feeds, and depth of cut. Records the wear of the milling insert, VB. The data set was provided by the UC Berkeley Emergent Space Tensegrities (BEST) Lab. 
**Download**: [Link](https://data.nasa.gov/download/vjv9-9f3x/application%2Fzip) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/3.+Milling.zip)  
**Data Set Citation**: A. Agogino and K. Goebel (UC Berkeley)

---

### 4. Bearings
**Description**: Accelerated life testing of bearings provided by the University of Cincinnati.  
Experiments on bearings. The data set was provided by the Center for Intelligent Maintenance Systems (IMS), University of Cincinnati.
**Download**: [Link](https://data.nasa.gov/download/brfb-gzcv/application%2Fzip) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/4.+Bearings.zip)  
**Data Set Citation**: J. Lee, et al. (University of Cincinnati)

---

### 5. Batteries
**Description**: Li-Ion battery experiments recording charging, discharging, and impedance under various temperatures.  
Experiments on Li-Ion batteries. Charging and discharging at different temperatures. Records the impedance as the damage criterion. The data set was provided by the NASA Prognostics Center of Excellence (PCoE).
**Download**: [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip)  
**Data Set Citation**: B. Saha and K. Goebel (NASA Ames Research Center)

---

### 6. Turbofan Engine Degradation Simulation
**Description**: Simulation data for turbofan engine degradation under various conditions and faults.
Engine degradation simulation was carried out using the Commercial Modular Aero-Propulsion System Simulation (C-MAPSS). Four different sets were simulated under different combinations of operational conditions and fault modes. This records several sensor channels to characterize fault evolution. The data set was provided by the NASA Ames Prognostics Center of Excellence (PCoE).  
**Download**: [Link](https://data.nasa.gov/Aeorspace/CMAPSS-Jet-Engine-Simulated-Data/ff5v-kuh6) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip)  
**Data Set Citation**: A. Saxena and K. Goebel (NASA Ames Research Center)

---

### 7. Prognostics Health Management 8 (PHM08) Challenge
**Description**: Data from the 2008 PHM data challenge for turbofan engines. Remaining Useful Life (RUL) is not revealed.  
Data from the data challenge competition held at the 1st international conference on Prognostics and Health Management (PHM08) is similar to the one posted above (see the Turbofan Engine Degradation Simulation data set) except the true Remaining Useful Life (RUL) values are not revealed. Users are expected to develop their algorithms using training and test sets provided in the package. The data set was provided by the NASA Prognostics Center of Excellence (PCoE).
**Download**: [Link](https://data.nasa.gov/download/nk8v-ckry/application%2Fzip)  
**Data Set Citation**: A. Saxena and K. Goebel (NASA Ames Research Center)
**Note**: 
  - Results should be formatted as a column vector of RULs in a text file.
  - Evaluation is limited to only one trial per day.

---

### 8. Insulated-Gate Bipolar Transistor (IGBT) Accelerated Aging
**Description**: Aging data of IGBTs under thermal overstress.  
Preliminary data from thermal overstress accelerated aging using the aging and characterization system. The data set contains aging data from 6 devices, one device aged with DC gate bias and the rest aged with a squared signal gate bias. Several variables are recorded and, in some cases, high-speed measurements of gate voltage, collector-emitter voltage, and collector current are available. The data set is provided by the NASA Prognostics Center of Excellence (PCoE).
**Download**: [Link](https://data.nasa.gov/download/7wwx-fk77/application%2Fzip) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/8.+IGBT+Accelerated+Aging.zip)  
**Data Set Citation**: J. Celaya, et al. (NASA Ames Research Center)

---

### 9. Trebuchet
**Description**: Trajectories of different types of balls launched from a trebuchet with varying counter weights. Flights were filmed and extraction routines calculated position of data. Both raw video data and extracted trajectories are provided. Geometry and physical properties of the trebuchet are available
**Download**: Data is currently unavailable for download directly. NASA is working to restore direct download capabilities. In the meantime, if you would like access to the data, please contact [christopher.a.teubert@nasa.gov
](christopher.a.teubert@nasa.gov)
**Data Set Citation**:  B. Morton. Sentient Corporation. “Trebuchet Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA

---

### 10. FEMTO Bearing
**Description**: Experiments on bearings’ accelerated life tests provided by FEMTO-ST Institute, Besançon, France. More information can be found here.
**Download**: [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/10.+FEMTO+Bearing.zip)
**Data Set Citation**: “FEMTO Bearing Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: P. Nectoux, R. Gouriveau, K. Medjaher, E. Ramasso, B. Morello, N. Zerhouni, C. Varnier. PRONOSTIA: An Experimental Platform for Bearings Accelerated Life Test. Institute of Electrical and Electronics Engineers (IEEE) International Conference on Prognostics and Health Management, Denver, CO, USA, 2012

---

### 11. Randomized Battery Usage
**Description**: Batteries are continuously cycled with randomly generated current profiles. Reference charging and discharging cycles are also performed after a fixed interval of randomized usage to provide reference benchmarks for battery state of health.
**Download**: Part 1 – Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-1-Random-Walk/ugxu-9kjx)
- Part 2 – Room Temperature Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-2-Room-Temperature-Random/qghr-qkfw)
- Part 3 – Room Temperate Variable Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-3-Room-Temperature-Variab/ed33-vxp2)
- Part 4 – 40C Right-Skewed Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-4-40C-Right-Skewed-Random/gah6-q2es)
- Part 5 – High-Temperature Right-Skewed Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-5-High-Temperature-Right-/tcjd-g74p)
- Part 6 – 40C Left-Skewed Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-6-40C-Left-Skewed-Random-/5uxu-h2h6)
- Part 7 – Low-Temperature Left-Skewed Random Walk: [link](https://data.nasa.gov/Raw-Data/Randomized-Battery-Usage-7-Low-Temperature-Left-Sk/sb48-rsbc) | [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/11.+Randomized+Battery+Usage+Data+Set.zip)
**Data Set Citation**: B. Bole, C. Kulkarni, and M. Daigle “Randomized Battery Usage Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: B. Bole, C. Kulkarni, and M. Daigle, ‘Adaptation of an Electrochemistry-based Li-Ion Battery Model to Account for Deterioration Observed Under Randomized Use’, Annual Conference of the Prognostics and Health Management Society, 2014

---

### 12. Capacitor Electrical Stress
**Description**: Capacitors were subjected to electrical stress under three voltage levels, i.e. 10V, 12V, and 14V. Data Set contains Electrical Impedance Spectroscopy (EIS) data as well as Charge/Discharge Signal data.
**Data Set Reference Document**: [link](http://www.femto-st.fr/en/Research-departments/AS2M/Research-groups/PHM/IEEE-PHM-2012-Data-challenge.php)
**Download**:[Mirror](https://phm-datasets.s3.amazonaws.com/NASA/12.+Capacitor+Electrical+Stress.zip)
**Data Set Citation**:  J. Renwick, C. Kulkarni, and J Celaya “Capacitor Electrical Stress Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: J. Renwick, C. Kulkarni and J. Celaya, “Analysis of Electrolytic Capacitor Degradation under Electrical Overstress for Prognostic Studies”, in the Proceedings of the Annual Conference of the Prognostics and Health Management Society, Coronado CA, October 2015

---

### 13. Metal-Oxide-Semiconductor Field-Effect Transistor (MOSFET) Thermal Overstress Aging
**Description**: Run-to-failure experiments on Power MOSFETs under thermal overstress.
**Data Set Reference Document**: Currently offline – email [link](christopher.a.teubert@nasa.gov)
**Download**:[Mirror](https://phm-datasets.s3.amazonaws.com/NASA/13.+MOSFET+Thermal+Overstress+Aging.zip)
**Data Set Citation**: J. R. Celaya, A. Saxena, S. Saha, and K. Goebel “MOSFET Thermal Overstress Aging Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: J. R. Celaya, A. Saxena, S. Saha, and K. Goebel, “Prognostics of Power MOSFETs under Thermal Stress Accelerated Aging using Data-Driven and Model-Based Methodologies,” in the Proceedings of the Annual Conference of the Prognostics and Health Management Society, (Montreal QC, Canada), September 2011.

---

### 14. Capacitor Electrical Stress-2
**Description**: Capacitors were subjected to electrical stress at 10V.
**Data Set Reference Document**: [link]( https://data.nasa.gov/api/views/y939-maf8/files/088396df-1ff9-4303-835f-5377cb4a710c?)
**Download**: [link](https://data.nasa.gov/download/y939-maf8/application%2Fzip) | [Mirror](Data is currently unavailable for download directly. NASA is working to restore direct download capabilities. In the meantime, if you would like access to the data, please contact [christopher.a.teubert@nasa.gov](christopher.a.teubert@nasa.gov))
**Data Set Citation**:  J. Celaya, C. Kulkarni, G. Biswas, and K. Goebel “Capacitor Electrical Stress Data Set – 2”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: J. Celaya, C. Kulkarni, G. Biswas, and K. Goebel, “Towards A Model-based Prognostics Methodology for Electrolytic Capacitors: A Case Study Based on Electrical Overstress Accelerated Aging”, International Journal of Prognostics and Health Management. 2012 Vol 3 (2) 004.

---

### 15. High-Intensity Radiated Field (HIRF) Battery
**Description**: Battery Data collected from the Experiments on the Edge 540 Aircraft in a HIRF Chamber.
**Data Set Reference Document**: Currently offline – email [christopher.a.teubert@nasa.gov](christopher.a.teubert@nasa.gov)
**Download**: [Mirror](https://phm-datasets.s3.amazonaws.com/NASA/15.+HIRF+Battery+Data+Set.zip)
**Data Set Citation**:  C. Kulkarni, E. Hogge, C. Quach and K. Goebel “HIRF Battery Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: Edward F. Hogge, Brian M. Bole, Sixto L. Vazquez, Jose Celaya,”Verification of a Remaining Flying Time Prediction System for Small Electric Aircraft”, Annual Conference of the Prognostics and Health Management, PHM 2015

---

### 16. Small Satellite Power Simulation
**Description**: Data collected from the simulated experiments on small satellite BP930 batteries using the MACCOR system.
**Data Set Reference Document**: [link]( https://data.nasa.gov/api/views/cpqc-ztjh/files/9fe7faeb-09e6-4d6d-9f5f-b0e23cd47c9b?download=true&filename=16.%20Description_of_Simulated_Small_Satellite_Operation_Data_Sets.pdf)
**Power Cycle Reference Sheet**: [link](https://data.nasa.gov/api/views/cpqc-ztjh/files/434a740e-ca14-4129-9070-df15af92c176?download=true&filename=16.%20Simulated_Current_Draw_Profile.xlsx) (you will need to cut & paste this link into your browser window)
**Download**: [link](https://data.nasa.gov/download/cpqc-ztjh/application%2Fzip) | Mirror- Data is currently unavailable for download directly. NASA is working to restore direct download capabilities. In the meantime, if you would like access to the data, please contact[christopher.a.teubert@nasa.gov](christopher.a.teubert@nasa.gov)
**Data Set Citation**: C. Kulkarni and A. Guarneros “Small Satellite Power Simulation Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: Z.Cameron, C. Kulkarni, A. Guarneros, K. Goebel and S.Poll, “A Battery Certification Testbed for Small Satellite Missions” , Institute of Electrical and Electronics Engineers (IEEE) AUTOTESTCON 2015, Nov 2-5, 2015, National Harbor, MA

---

### 17. Turbofan Engine Degradation Simulation-2
**Description**: The generation of data-driven prognostics models requires the availability of data sets with run-to-failure trajectories. To contribute to the development of these methods, the data set provides a new realistic data set of run-to-failure trajectories for a small fleet of aircraft engines under realistic flight conditions. The damage propagation modelling used for the generation of this synthetic data set builds on the modeling strategy from previous work. The data set was generated with the Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) dynamical model. The data set has been provided by the NASA Prognostics Center of Excellence (PCoE) in collaboration with ETH Zurich and PARC.
**Download**: [Mirror]( https://phm-datasets.s3.amazonaws.com/NASA/17.+Turbofan+Engine+Degradation+Simulation+Data+Set+2.zip)
**Data Set Citation**: M. Chao, C.Kulkarni, K. Goebel and O. Fink (2021). “Aircraft Engine Run-to-Failure Dataset under real flight conditions”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA

---

### 18. Fatigue Crack Growth in Aluminum Lap Joint
**Description**: Fatigue experiments were conducted on aluminum lap-joint specimens, and lamb wave signals were recorded for each specimen at several time points (i.e., defined as number of cycles in fatigue testing). Signals from piezo actuator-receiver sensor pairs were reported and it was observed that these signals were directly related to the crack lengths developed during fatigue testing. Optical measurements of surface crack lengths are also provided as the ground truth. The data set is split in training and validation to facilitate the application of data-driven methods. This data set was generated at Arizona State University by Prof. Yongming Liu, Dr. Tishun Peng, and their collaborators. The data set was used for the Prognostics Health Management (PHM) Data Challenge for the 2019 Conference on Prognostics and Health Management. Other than the data set authors, the following people helped put together the 2019 PHM data challenge and make the data set publicly available. Matteo Corbetta and Portia Banerjee (KBR, Inc, NASA Ames), Kurt Doughty (Collins Aerospace), Kai Goebel (PARC), and Scott Clements (Lockheed Martin).
**Download**: [link](https://data.nasa.gov/download/awzu-cpt8/application%2Fzip)
**Data Set Citation**: Peng T, He J, Xiang Y, Liu Y, Saxena A, Celaya J, Goebel K. Probabilistic fatigue damage prognosis of lap joint using Bayesian updating. Journal of Intelligent Material Systems and Structures. 2015 May;26(8):965-79.
**Publication Citation**: He J, Guan X, Peng T, Liu Y, Saxena A, Celaya J, Goebel K. A multi-feature integration method for fatigue crack detection and crack length estimation in riveted lap joints using Lamb waves. Smart Materials and Structures. 2013 Sep 4;22(10):105007.

---

### 19. CNC Milling Machine
**Description**: Remaining Useful Life (RUL) estimation for high-speed CNC milling machine cutters using dynamometer, accelerometer, and acoustic emission data. This data was used in the 2010 Prognostics Health Management (PHM) Society Data Competition.
**Download**: [Mirror](https://phmsociety.org/phm_competition/2010-phm-society-conference-data-challenge/)

---

### 20. Anemometer
**Description**: Data set for cup anemometers. This data was used in the 2011 Prognostics Health Management (PHM) Society Data Competition.
**Download**: [link](https://phmsociety.org/phm11-data-challenge-condition-monitoring-of-anemometers/) | [Mirror](https://phmsociety.org/phm_competition/2011-phm-society-conference-data-challenge/)

---

### 21. Accelerated Battery Life Testing
**Description**: This data set presents accelerated-Li-ion battery lifecycle data focused on a large range of load levels and the characterization of the lifecycle of a battery pack composed of two 18650 battery cells. The lifecycle study is conducted with a total of 26 battery packs that are grouped by constant and random loading conditions, loading levels, and number of load-level changes. The data also includes load cycling on second-life batteries, where surviving cells from previously aged battery packs were assembled for second- life packs.
**Download**: [link](https://data.nasa.gov/download/xg3n-ngei/application%2Fzip)
**Data Set Citation**: Fricke, K., Nascimento, R., Corbetta, M., Kulkarni, C., & Viana, F. “Accelerated Battery Life Testing Dataset”, NASA Prognostics Data Repository, Probabilistic Mechanics Lab, University of Central Florida, and NASA Ames Research Center, Moffett Field, CA
**Publication Citation**: Fricke, K., Nascimento, R., Corbetta, M., Kulkarni, C., & Viana, F. (2023). Prognosis of Li-ion Batteries Under Large Load Variations Using Hybrid Physics-Informed Neural Networks. Annual Conference of the PHM Society, 15(1). https://doi.org/10.36001/phmconf.2023.v15i1.3463

---  

This data set was generated from a custom-made testbed to cycle battery packs designed and developed by Kajetan Fricke, Renato Nascimento, and Professor Felipe Viana from the Probabilistic Mechanics Laboratory at the University of Central Florida (UCF). This work is the result of a collaboration between the Probabilistic Mechanics Lab at the University of Central Florida, and the Intelligent Systems Division Diagnostics & Prognostics Group at NASA Ames Research Center.

For more information, visit the [NASA Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/).