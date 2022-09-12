import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(0.109),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         crossSection = cms.untracked.double(1430000.0),
                         comEnergy = cms.double(13600.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             processParameters = cms.vstring(
                                'Bottomonium:all = on',                     # Quarkonia, MSEL=62, allow feed-down
                                '553:onMode = off',                          # Turn off all J/psi decays
                                '553:onIfMatch = 13 -13',                    # Tun on J/psi -> mu+ mu-
                                'PhaseSpace:pTHatMin = 5.0'                 # ckin(3), be aware of this
                             ),
                             parameterSets = cms.vstring('pythia8CommonSettings',
                                'pythia8CP5Settings',
                                'processParameters',
                             )
                         ),

)

# Filter any upsilon(NS) with pT > 11 GeV and |eta| < 1.5

mumufilter = cms.EDFilter("PythiaDauVFilter",
        MotherID = cms.untracked.int32(0),
        MinPt = cms.untracked.vdouble(3.0,3.0),
        ParticleID = cms.untracked.int32(553),
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
    MinPt = cms.untracked.double(9.0),
    ParticleID = cms.untracked.int32(553)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumufilter)

