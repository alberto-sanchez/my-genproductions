import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(0.109),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         crossSection = cms.untracked.double(1430000.0),
                         comEnergy = cms.double(13600.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
                             EvtGen130 = cms.untracked.PSet(
                                list_forced_decays = cms.vstring('MyUpsilon'),
                                decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                                particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                                operates_on_particles = cms.vint32(553),
                                convertPythiaCodes = cms.untracked.bool(False),
                                user_decay_embedded = cms.vstring(
'''
Alias MyUpsilon Upsilon
ChargeConj MyUpsilon MyUpsilon

Decay MyUpsilon
1.0000  mu+        mu-                 PHOTOS VLL ;
Enddecay

End
'''
                                )                    
                             ),
                             parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             processParameters = cms.vstring(
                                'Bottomonium:all = on',                     # Quarkonia, MSEL=62, allow feed-down
                                'PhaseSpace:pTHatMin = 7.0'                 # ckin(3), be aware of this
                             ),
                             parameterSets = cms.vstring('pythia8CommonSettings',
                                'pythia8CP5Settings',
                                'processParameters',
                             )
                         ),

)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

# Filter any upsilon(NS) with pT > 11 GeV and |eta| < 1.5

mumufilter = cms.EDFilter("PythiaDauVFilter",
        MotherID = cms.untracked.int32(0),
        MinPt = cms.untracked.vdouble(4.0,4.0),
        ParticleID = cms.untracked.int32(553),
        ChargeConjugation = cms.untracked.bool(False),
        MinEta = cms.untracked.vdouble(-1.5,-1.5),
        MaxEta = cms.untracked.vdouble(1.5,1.5),
        NumberDaughters = cms.untracked.int32(2),
        DaughterIDs = cms.untracked.vint32(13, -13)
)

oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxRapidity = cms.untracked.double(1.3),
    MinRapidity = cms.untracked.double(-1.3),
    MinPt = cms.untracked.double(11.0),
    ParticleID = cms.untracked.int32(553)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumufilter)

