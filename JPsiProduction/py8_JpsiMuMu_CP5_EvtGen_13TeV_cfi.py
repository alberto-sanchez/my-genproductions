import FWCore.ParameterSet.Config as cms

from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            convertPythiaCodes = cms.untracked.bool(False),   # required for later versions of evtgen
            operates_on_particles = cms.vint32(443),          # use EvtGen just for signal particle decay
            list_forced_decays = cms.vstring('MyJ/psi'),
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_embedded = cms.vstring(
'''
Alias MyJ/psi J/psi
ChargeConj MyJ/psi MyJ/psi

Decay MyJ/psi
1.0000  mu+        mu-                 PHOTOS VLL ;
Enddecay

End
'''
           )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Charmonium:all = on',                       # Quarkonia, MSEL=61, including feed-down as well
            'PhaseSpace:pTHatMin = 15.'                  # this cut should around 10 GeV below the actual cut on Onia
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)   # Required by EvtGen

# Filter with high pT cut on dimuon, trying to accomodate trigger requirements.

mumufilter = cms.EDFilter("PythiaDauVFilter",
        MotherID = cms.untracked.int32(0),
        MinPt = cms.untracked.vdouble(4.0,4.0),
        ParticleID = cms.untracked.int32(443),
        ChargeConjugation = cms.untracked.bool(False),
        MinEta = cms.untracked.vdouble(-1.5,-1.5),
        MaxEta = cms.untracked.vdouble(1.5,1.5),
        NumberDaughters = cms.untracked.int32(2),
        DaughterIDs = cms.untracked.vint32(13, -13)
)

oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxRapidity = cms.untracked.double(1.5),
    MinRapidity = cms.untracked.double(-1.5),
    MinPt = cms.untracked.double(24.0),
    ParticleID = cms.untracked.int32(443)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumufilter)
