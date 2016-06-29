import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(0.00013),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         crossSection = cms.untracked.double(54710000000.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         comEnergy = cms.double(13000.0),
                         ExternalDecays = cms.PSet(
                            EvtGen130 = cms.untracked.PSet(
                               decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
                               particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
                               user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Onia_mumu.dec'),
                               list_forced_decays = cms.vstring('MyJ/psi'),
                               operates_on_particles = cms.vint32()
                            ),
                            parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                            pythia8CUEP8M1SettingsBlock,
                            pythia8CommonSettings = cms.vstring(
                               'Tune:preferLHAPDF = 2',
                               'Main:timesAllowErrors = 10000',
                               'Check:epTolErr = 0.01',
                               'Beams:setProductionScalesFromLHEF = off',
                               'SLHA:keepSM = on',
                               'SLHA:minMassSM = 1000.',
                               'ParticleDecays:limitTau0 = on',
                               'ParticleDecays:tau0Max = 10',
                               'ParticleDecays:allowPhotonRadiation = off',  # Turn on/off QED FSR, see pythia8CommonSettings
                            ),
                            processParameters = cms.vstring('HardQCD:all = on'),
                            parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                            )
                         )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bfilter = cms.EDFilter("PythiaFilter",
                       ParticleID = cms.untracked.int32(5)
                       )

jpsifilter = cms.EDFilter("PythiaFilter",
                          Status = cms.untracked.int32(2),
                          MaxEta = cms.untracked.double(1000.0),
                          MinEta = cms.untracked.double(-1000.0),
                          MinPt = cms.untracked.double(3.0),
                          ParticleID = cms.untracked.int32(443)
                          )

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
                             Status = cms.untracked.vint32(1, 1),
                             MinPt = cms.untracked.vdouble(0.5, 0.5),
                             MinP = cms.untracked.vdouble(0., 0.),
                             MaxEta = cms.untracked.vdouble(2.5, 2.5),
                             MinEta = cms.untracked.vdouble(-2.5, -2.5),
                             ParticleCharge = cms.untracked.int32(-1),
                             MaxInvMass = cms.untracked.double(4.0),
                             MinInvMass = cms.untracked.double(2.0),
                             ParticleID1 = cms.untracked.vint32(13),
                             ParticleID2 = cms.untracked.vint32(13)
                             )

ProductionFilterSequence = cms.Sequence(generator*bfilter*jpsifilter*mumugenfilter)

