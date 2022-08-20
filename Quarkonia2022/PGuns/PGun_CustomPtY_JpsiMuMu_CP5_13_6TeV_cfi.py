import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8TFuncPtYGun",
    PGunParameters = cms.PSet(
        MaxPt  = cms.double(150.0),
        MinPt  = cms.double(19.0),
        MaxY   = cms.double(3.0),
        MinY   = cms.double(-3.0),
        MaxPhi = cms.double(3.14159265359),
        MinPhi = cms.double(-3.14159265359),
        ParticleID       = cms.vint32(443),
        AddAntiParticle  = cms.bool(False),
        TFunction_string = cms.string('x*((1.+x*x/((3.274-2.)*3.221))^(-3.274))')
    ),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity  = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            '443:onMode = off',                          # Turn off all J/psi decays
            '443:onIfMatch = 13 -13',                    # Tun on J/psi -> mu+ mu-
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

ProductionFilterSequence = cms.Sequence(generator)
