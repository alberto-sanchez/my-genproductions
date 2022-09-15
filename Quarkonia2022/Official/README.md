# my-genproductions / Quarkonia2022 / Official

Configuration files used for official request under Summer22 campaign


**Setup: Summer 2022 recipe**

```
#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc10
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_8/src ] ; then
  echo release CMSSW_12_4_8 already exists
else
  scram p CMSSW CMSSW_12_4_8
fi
cd CMSSW_12_4_8/src
eval `scram runtime -sh`

# if needed use other cfg
pyfile=BPH-Run3Summer22GS-00011

curl -s --insecure \
https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/Quarkonia2022/Official/${pyfile}.py \
--retry 2 --create-dirs -o Configuration/GenProduction/python/${pyfile}.py
[ -s Configuration/GenProduction/python/${pyfile}.py ] || exit $?;

scram b
cd ../..

EVENTS=100000

#GEN-SIM
cmsDriver.py Configuration/GenProduction/python/${pyfile} --python_filename ${pyfile}_1_cfg.py --eventcontent RAWSIM \
--customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:${pyfile}_1.root --conditions 124X_mcRun3_2022_realistic_v11 \
--beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n $EVENTS || exit $? ;

#GEN
cmsDriver.py Configuration/GenProduction/python/${pyfile} --python_filename ${pyfile}_0_cfg.py --eventcontent RAWSIM \
--customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --fileout file:${pyfile}_0.root --conditions 124X_mcRun3_2022_realistic_v11 \
--beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN --geometry DB:Extended --era Run3 --no_exec --mc -n $EVENTS || exit $? ;

```

