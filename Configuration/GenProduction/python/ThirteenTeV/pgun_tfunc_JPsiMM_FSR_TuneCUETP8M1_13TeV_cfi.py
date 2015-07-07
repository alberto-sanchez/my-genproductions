import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8PtGunTFunc",
    maxEventsToPrint = cms.untracked.int32(5),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    PGunParameters = cms.PSet(
        MaxPt = cms.double(120.),
        MinPt = cms.double(10.),
        ParticleID = cms.vint32(443),
        AddAntiParticle = cms.bool(False), 
        MaxEta = cms.double(1.2),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-1.2),
        MinPhi = cms.double(-3.14159265359), ## in radians
        TFunction_string = cms.string('x*((1.+1./(3.357-2.)*x*x/2.085)^(-3.357))'),
        TFunction_min = cms.double(10.),
        TFunction_max = cms.double(120.),
   ),
   PythiaParameters = cms.PSet(
       pythia8CommonSettingsBlock,
       pythia8CUEP8M1SettingsBlock,
       pythiaJpsiDecays = cms.vstring(
            '443:onMode = off',                          # Turn off J/psi decays
            '443:onIfMatch = 13 -13',                    # just let J/psi -> mu+ mu-
       ),
       parameterSets = cms.vstring('pythia8CommonSettings',
                                   'pythia8CUEP8M1Settings',
                                   'pythiaJpsiDecays')
   )
)

ProductionFilterSequence = cms.Sequence(generator)
