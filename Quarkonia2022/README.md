# my-genproductions / Quarkonia2022
Be aware that this configs have being tested just for the official MC Campaign Run3Winter22, other
branches may work but it is not warranty. For testing porpouses always try to use the latest
version in either branch.


**Setup: 2022 conditions**

```
#!/bin/bash
source  /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
if [ -r CMSSW_12_2_4/src ] ; then
 echo release CMSSW_12_2_4 already exists
else
scram p CMSSW CMSSW_12_2_4
fi
cd CMSSW_12_2_4/src
eval `scram runtime -sh`

pydir=Configuration/GenProduction/python
pyfile=py8_JpsiMuMu_CP5_13TeV_cfi.py

curl -s --insecure \
https://raw.githubusercontent.com/alberto-sanchez/my-genproductions/master/Quarkonia2022/$pyfile \
--retry 2 --create-dirs -o $pydir/$pyfile

scram b
cd ../../

cmsDriver.py $pydir/$pyfile  --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:gen_sim.root --conditions 122X_mcRun3_2021_realistic_v9 --beamspot Run3RoundOptics25ns13TeVLowSigmaZ --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc --python_filename step0_cfg.py -n 50000 || exit $? ;

