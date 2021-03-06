import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(0.109),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         crossSection = cms.untracked.double(1430000.0),
                         comEnergy = cms.double(13000.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
                             EvtGen130 = cms.untracked.PSet(
                                decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                                particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                                operates_on_particles = cms.vint32(553,100553,200553),              
                                convertPythiaCodes = cms.untracked.bool(False)
                             ),
                             parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
                             pythia8CP5SettingsBlock,
                             processParameters = cms.vstring(
                                'Bottomonium:all = on',                     # Quarkonia, MSEL=62, allow feed-down
                                'PhaseSpace:pTHatMin = 5.0'                 # ckin(3), be aware of this
                             ),
                             parameterSets = cms.vstring('pythia8CommonSettings',
                                'pythia8CP5Settings',
                                'processParameters',
                             )
                         ),

)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

# Filter any upsilon(NS) with pT > 9 GeV and |eta| < 1.4
 
oniafilter = cms.EDFilter("MCMultiParticleFilter",
     Status = cms.vint32(2, 2, 2),
     ParticleID = cms.vint32(553,100553,200553),
     PtMin = cms.vdouble(9.,9.,9.),
     NumRequired = cms.int32(1),
     EtaMax = cms.vdouble(1.4,1.4,1.4),
     EtaMin = cms.vdouble(-1.4,-1.4,-1.4),
     AcceptMore = cms.bool(True)
)

# Filter a dimuon decay of the upsilon(NS) above with pT of muons > 3 GeV

mufilter = cms.EDFilter("MCMultiParticleFilter",
     Status = cms.vint32(1, 1, 1),
     ParticleID = cms.vint32(13,13,13),
     MotherID = cms.untracked.vint32(553,100553,200553),
     PtMin = cms.vdouble(3.,3.,3.),
     NumRequired = cms.int32(2),
     EtaMax = cms.vdouble(99.,99.,99.),
     EtaMin = cms.vdouble(-99.,-99.,-99.),
     AcceptMore = cms.bool(True)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mufilter)
