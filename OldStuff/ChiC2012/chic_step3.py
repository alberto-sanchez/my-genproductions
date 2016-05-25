debug_filename = 'debug.txt'

import FWCore.ParameterSet.Config as cms

process = cms.Process('test')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load('MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.GlobalTag.globaltag = cms.string('START53_V15A::All')

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.destinations = cms.untracked.vstring(debug_filename)
#process.MessageLogger.cout = process.MessageLogger.cerr
#process.MessageLogger.cout.threshold = cms.untracked.string("DEBUG")

output_filename = 'step3.root'

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring('step2.root')
    )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

process.triggerSelection = cms.EDFilter("TriggerResultsFilter",
                                        triggerConditions = cms.vstring( 'HLT_Dimuon8_Jpsi_v*' ),
                                        hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                                        l1tResults = cms.InputTag( "gtDigis" ),
                                        l1tIgnoreMask = cms.bool( False ),
                                        l1techIgnorePrescales = cms.bool( False ),
                                        daqPartitions = cms.uint32( 1 ),
                                        throw = cms.bool( True )
                                        )

process.load('Ponia.Modules.CHARM_chiCandProducer_cff')

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(output_filename),
    outputCommands =  cms.untracked.vstring('drop *',
					    'keep *_offlinePrimaryVertices_*_*',
#					    Temporary, testing if it solves excessive use of ram in chic analysis
                                            'keep *_dimuonProducer_UpsilonCandLorentzVector_*',
                                            'keep *_chiCandProducer_chicand_*',
					    'keep *_chiCandProducer_piZeroRejectCand_*',
					    'keep *_refit_*_*',
#                                           This are for mc
                                            'keep *_genParticles_*_*',
                                            'keep *_g4SimHits__*'
                                            ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p'))
    )

process.end = cms.EndPath(process.out)

process.p = cms.Path(process.triggerSelection*process.chiSequence)
process.schedule = cms.Schedule(process.p,process.end)

# HACK ! Need to understand !
process.dimuonProducer.addMuonlessPrimaryVertex = False
