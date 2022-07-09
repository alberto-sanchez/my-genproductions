# my-genproductions / Quarkonia2022 / Summer22
Be aware that this configs have being tested just for the official MC Campaign Run3Summer22, other
branches may work but it is not warranty. For testing porpouses always try to use the latest
version in either branch.


**Setup: Summer 2022 conditions**

```
#!/bin/bash
source  /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
if [ -r CMSSW_12_4_2/src ] ; then
 echo release CMSSW_12_4_2 already exists
else
scram p CMSSW CMSSW_12_4_2
fi
cd CMSSW_12_4_2/src
eval `scram runtime -sh`

pydir=Configuration/GenProduction/python
pyfile=py8_JpsiMuMu_CP5_13_6TeV_cfi.py

curl -s --insecure \
https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/Quarkonia2022/Summer22/$pyfile \
--retry 2 --create-dirs -o $pydir/$pyfile

scram b
cd ../../

#GEN-SIM
cmsDriver.py $pydir/$pyfile  --python_filename step0_cfg.py --eventcontent RAWSIM \
--customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM \
--fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v8 \
--beamspot Run3RoundOptics25ns13TeVLowSigmaZ --step GEN,SIM --geometry DB:Extended \
--era Run3 --no_exec --mc -n 10000 || exit $? ;

#GEN
cmsDriver.py $pydir/$pyfile  --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier GEN --fileout file:gen.root --conditions 124X_mcRun3_2022_realistic_v8 \
--beamspot Run3RoundOptics25ns13TeVLowSigmaZ --step GEN --geometry DB:Extended --era Run3 --no_exec --mc \
--python_filename gen_cfg.py -n 100000 || exit $? ;
