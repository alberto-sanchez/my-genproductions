# cfg file for Chi_{b1,b2}(3P) -> Upsilon(3S) gamma,  we are neglecting Chi_b0. Masses and widths are matched between pythia, evtgen and PDG 2016
# a mass separation between Chi_b1 and Chi_b2 is assumed to be 10.4 MeV  
#
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('mychi_b1','mychi_b2'),        # will force one at the time
            operates_on_particles = cms.vint32(20553,555),                  # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Particle Upsilon 9.4603000 0.00005402
Particle chi_b1 10.512100 0.00000
Particle chi_b2 10.522500 0.00000

Alias myUpsilon Upsilon
Alias mychi_b1 chi_b1
Alias mychi_b2 chi_b2

Decay myUpsilon
1.0   mu+  mu-          PHOTOS  VLL;
Enddecay

Decay mychi_b1
1.0   gamma  myUpsilon  HELAMP 1. 0. 1. 0. -1. 0. -1. 0.;
Enddecay

Decay mychi_b2
1.0   gamma  myUpsilon  PHSP;
Enddecay

End
"""
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3PJ) = 20553,555',
            'Bottomonium:O(3PJ)[3P0(1)] = 0.085,0.085',
            'Bottomonium:O(3PJ)[3S1(8)] = 0.04,0.04',
            'Bottomonium:gg2bbbar(3PJ)[3PJ(1)]g = on,on',
            'Bottomonium:qg2bbbar(3PJ)[3PJ(1)]q = on,on',
            'Bottomonium:qqbar2bbbar(3PJ)[3PJ(1)]g = on,on',
            'Bottomonium:gg2bbbar(3PJ)[3S1(8)]g = on,on',
            'Bottomonium:qg2bbbar(3PJ)[3S1(8)]q = on,on',
            'Bottomonium:qqbar2bbbar(3PJ)[3S1(8)]g = on,on',
            'PhaseSpace:pTHatMin = 2.',
            '20553:m0 = 10.512100',
            '555:m0 = 10.522500',
            '20553:onMode = off',
            '555:onMode = off'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
    )
)

# We will filter for chi_b1, and chi_b2, first on the ID, then in the mass, this will constraint the photon daughter

pwaveIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(20553,555),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    MinEta = cms.untracked.vdouble(-9., -9.),
    MaxEta = cms.untracked.vdouble(9., 9.),
    Status = cms.untracked.vint32(2, 2)
)

pwaveMassfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(2, 1),
    MinPt = cms.untracked.vdouble(6., 0.2),
    MaxEta = cms.untracked.vdouble(9., 3.),
    MinEta = cms.untracked.vdouble(-9., -3.),
    ParticleCharge = cms.untracked.int32(0),
    MinP = cms.untracked.vdouble(0.,0.),
    ParticleID1 = cms.untracked.vint32(553),
    ParticleID2 = cms.untracked.vint32(22),
    MinInvMass = cms.untracked.double(10.51),
    MaxInvMass = cms.untracked.double(10.53),
)

# Next two muon filter are derived from muon reconstruction

muminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.5, 0.5, 1.5, 1.5, 2.5),
    ParticleID = cms.untracked.int32(553),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(1.6, -2.4, 1.2, -1.6, -1.2),
    MaxEta = cms.untracked.vdouble(2.4, -1.6, 1.6, -1.2, 1.2),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(-13, -13, -13, -13, -13)
)

muplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.5, 0.5, 1.5, 1.5, 2.5),
    ParticleID = cms.untracked.int32(553),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(1.6, -2.4, 1.2, -1.6, -1.2),
    MaxEta = cms.untracked.vdouble(2.4, -1.6, 1.6, -1.2, 1.2),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(13, 13, 13, 13, 13)
)

ProductionFilterSequence = cms.Sequence(generator*pwaveIDfilter*pwaveMassfilter*muminusfilter*muplusfilter)
