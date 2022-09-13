import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Charmonium:all = on',                       # Quarkonia, MSEL=61, including feed-down
            '443:onMode = off',                          # Turn off all J/psi decays
            '443:onIfMatch = 13 -13',                    # Tun on J/psi -> mu+ mu-
            'PhaseSpace:pTHatMin = 19.'                  # should be 5 GeV below the actual cut
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

# Filter with high pT cut on dimuon, trying to accomodate trigger requirements.

mumufilter = cms.EDFilter("PythiaDauVFilter",
        MotherID = cms.untracked.int32(0),
        MinPt = cms.untracked.vdouble(3.0,3.0),
        ParticleID = cms.untracked.int32(443),
        ChargeConjugation = cms.untracked.bool(False),
        MinEta = cms.untracked.vdouble(-2.4,-2.4),
        MaxEta = cms.untracked.vdouble(2.4,2.4),
        NumberDaughters = cms.untracked.int32(2),
        DaughterIDs = cms.untracked.vint32(13, -13)
)

oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxRapidity = cms.untracked.double(1.3),
    MinRapidity = cms.untracked.double(-1.3),
    MinPt = cms.untracked.double(24.0),
    ParticleID = cms.untracked.int32(443)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumufilter)
