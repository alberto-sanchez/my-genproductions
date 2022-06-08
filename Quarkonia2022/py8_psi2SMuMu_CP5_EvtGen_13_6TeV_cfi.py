import FWCore.ParameterSet.Config as cms
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            convertPythiaCodes = cms.untracked.bool(False),   # required for later versions of evtgen
            operates_on_particles = cms.vint32(100443),          # use EvtGen just for signal particle decay
            list_forced_decays = cms.vstring('MyPsi2S'),
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_embedded = cms.vstring(
'''
Alias MyPsi2S psi(2S)
ChargeConj MyPsi2S MyPsi2S

Decay MyPsi2S
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
    comEnergy = cms.double(13600.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
                'Charmonium:states(3S1) = 100443',
                'Charmonium:O(3S1)[3S1(1)] = 0.76',
                'Charmonium:O(3S1)[3S1(8)] = 0.0050',
                'Charmonium:O(3S1)[1S0(8)] = 0.004',
                'Charmonium:O(3S1)[3P0(8)] = 0.004',
                'Charmonium:gg2ccbar(3S1)[3S1(1)]g = on',
                'Charmonium:gg2ccbar(3S1)[3S1(1)]gm = on',
                'Charmonium:gg2ccbar(3S1)[3S1(8)]g = on',
                'Charmonium:qg2ccbar(3S1)[3S1(8)]q = on',
                'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on',
                'Charmonium:gg2ccbar(3S1)[1S0(8)]g = on',
                'Charmonium:qg2ccbar(3S1)[1S0(8)]q = on',
                'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = on',
                'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = on',
                'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = on',
                'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = on',
                'PhaseSpace:pTHatMin = 5.'
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
        MinPt = cms.untracked.vdouble(4.0,4.0),
        ParticleID = cms.untracked.int32(100443),
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
    MinPt = cms.untracked.double(9.0),
    ParticleID = cms.untracked.int32(100443)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumufilter)
