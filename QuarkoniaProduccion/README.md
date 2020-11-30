# my-genproductions / QuarkoniaProduccion
Be aware that this configs have being tested just for the official MC branch 7_1_x, 9_3_x, 10_2,x for runII for other
branches may work but it is not warranty. For testing porpouses always try to use the latest
version in either branch.


**Setup: 2016 conditions**

```
#!/bin/bash
source  /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
if [ -r CMSSW_7_1_46/src ] ; then
 echo release CMSSW_7_1_46 already exists
else
scram p CMSSW CMSSW_7_1_46
fi
cd CMSSW_7_1_46/src
eval `scram runtime -sh`

pydir=Configuration/GenProduction/python
pyfile=py8_JpsiMuMu_CP5_13TeV_cfi.py

curl -s --insecure \
https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/QuarkoniaProduccion/$pyfile \
--retry 2 --create-dirs -o $pydir/$pyfile

scram b
cd ../../
cmsDriver.py $pydir/$pyfile --fileout file:gen_sim.root --mc --eventcontent RAWSIM \
--customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring \
--datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 \
--python_filename step0_cfg.py --no_exec -n 50000
```


**Setup: 2017 conditions**

```
#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc630
if [ -r CMSSW_9_3_10/src ] ; then
 echo release CMSSW_9_3_10 already exists
else
scram p CMSSW CMSSW_9_3_10
fi
cd CMSSW_9_3_10/src
eval `scram runtime -sh`

pyfile=py8_JpsiMuMu_CP5_13TeV_cfi.py
pydir=Configuration/GenProduction/python
myurl=https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/QuarkoniaProduccion/$pyfile

curl -s --insecure $myurl/$pyfile --retry 2 --create-dirs -o $pydir/$pyfile
[ -s ${pyfile} ] || exit $?;

scram b

cd ../../
cmsDriver.py $pydir/$pyfile --fileout file:gensim.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 \
--beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --geometry DB:Extended --era Run2_2017 --python_filename step0_cfg.py \
--no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 50000 || exit $? ;
```

**Setup: 2018 conditions**

```
#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700
if [ -r CMSSW_10_2_7/src ] ; then
 echo release CMSSW_10_2_7 already exists
else
scram p CMSSW CMSSW_10_2_7
fi
cd CMSSW_10_2_7/src
eval `scram runtime -sh`

pyfile=py8_JpsiMuMu_CP5_13TeV_cfi.py
pydir=Configuration/GenProduction/python
myurl=https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/QuarkoniaProduccion/$pyfile

curl -s --insecure $myurl/$pyfile --retry 2 --create-dirs -o $pydir/$pyfile
[ -s ${pyfile} ] || exit $?;

scram b

cd ../../
cmsDriver.py $pydir/$pyfile --fileout file:gensim.root  --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v11 \
--beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --geometry DB:Extended --era Run2_2018 --python_filename step0_cfg.py \
--no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 50000 || exit $? ;



