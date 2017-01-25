import FWCore.ParameterSet.Config as cms
from Configuration.Generator.PythiaUEZ2starSettings_cfi import *

generator = cms.EDFilter(
    "Pythia6GeneratorFilter",
    comEnergy = cms.double(8000.0),
    crossSection = cms.untracked.double(48440000000),
    filterEfficiency = cms.untracked.double(5.2e-5),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),

    PythiaParameters = cms.PSet(
    pythiaUESettingsBlock,
        bbbarSettings = cms.vstring('MSEL = 1'),
        parameterSets = cms.vstring(
             'pythiaUESettings',
             'bbbarSettings')

    )
    )

TwoMuonFilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1,1),
    MinPt = cms.untracked.vdouble(0.0,0.0),
    MaxPt = cms.untracked.vdouble(4000.0,4000.0),
    MaxEta = cms.untracked.vdouble( 10.,10.),
    MinEta = cms.untracked.vdouble(-10.,-10.),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(-13),
    MinInvMass = cms.untracked.double(8.5),
    MaxInvMass = cms.untracked.double(11.5),
)

ProductionFilterSequence = cms.Sequence(generator*TwoMuonFilter)
