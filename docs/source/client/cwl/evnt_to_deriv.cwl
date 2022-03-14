cwlVersion: v1.0
class: Workflow

inputs: []

outputs:
  outDS:
    type: string
    outputSource: deriv/outDS


steps:
  evnt:
    run: prun
    in:
      opt_exec:
        default: "Generate_tf.py --maxEvents=%MAXEVENTS --ecmEnergy=13000 --evgenJobOpts=MC15JobOpts-01-01-86_v2.tar.gz --firstEvent=%FIRSTEVENT:1 --jobConfig=MC15JobOptions/MC15.312766.MadGraphPythia8EvtGen_A14NNPDF23LO_zp2hdm_bb_mzp1200_mA700.py --outputEVNTFile=EVNT.pool.root.1 --randomSeed=%RNDM:100 --runNumber=312766 --AMITag=e7845"
      opt_args:
        default: "--outputs EVNT.pool.root.1 --nEvents=2000 --nJobs 2 --athenaTag MCProd,20.7.9.9.27 --noBuild --expertOnly_skipScout --avoidVP"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  simul:
    run: prun
    in:
      opt_inDS: evnt/outDS
      opt_exec:
        default: "Sim_tf.py --inputEVNTFile=%IN --maxEvents=%MAXEVENTS --postInclude default:RecJobTransforms/UseFrontier.py --preExec 'EVNTtoHITS:simFlags.SimBarcodeOffset.set_Value_and_Lock(200000)' 'EVNTtoHITS:simFlags.TRTRangeCut=30.0;simFlags.TightMuonStepping=True' --preInclude EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py --skipEvents=%SKIPEVENTS --firstEvent=%FIRSTEVENT:1 --outputHITSFile=HITS.pool.root.1 --physicsList=FTFP_BERT_ATL_VALIDATION --randomSeed=%RNDM:1 --DBRelease=all:current --conditionsTag default:OFLCOND-MC16-SDR-14 --geometryVersion=default:ATLAS-R2-2016-01-00-01_VALIDATION --runNumber=312806 --AMITag=s3126 --DataRunNumber=284500 --simulator=FullG4 --truthStrategy=MC15aPlus"
      opt_args:
        default: "--outputs HITS.pool.root.1 --nEventsPerFile=10 --nEventsPerJob 5 --athenaTag AtlasOffline,21.0.15 --noBuild --expertOnly_skipScout --avoidVP"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  pile:
    run: prun
    in:
      opt_inDS: simul/outDS
      opt_exec:
        default: "Reco_tf.py --inputHITSFile=%IN --maxEvents=10 --postExec 'all:CfgMgr.MessageSvc().setError+=[\"HepMcParticleLink\"]' 'ESDtoAOD:fixedAttrib=[s if \"CONTAINER_SPLITLEVEL = '\"'\"'99'\"'\"'\" not in s else \"\" for s in svcMgr.AthenaPoolCnvSvc.PoolAttributes];svcMgr.AthenaPoolCnvSvc.PoolAttributes=fixedAttrib' --postInclude default:PyJobTransforms/UseFrontier.py --preExec 'all:rec.Commissioning.set_Value_and_Lock(True);from AthenaCommon.BeamFlags import jobproperties;jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0);from LArROD.LArRODFlags import larRODFlags;larRODFlags.NumberOfCollisions.set_Value_and_Lock(20);larRODFlags.nSamples.set_Value_and_Lock(4);larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True);larRODFlags.firstSample.set_Value_and_Lock(0);larRODFlags.useHighestGainAutoCorr.set_Value_and_Lock(True); from LArDigitization.LArDigitizationFlags import jobproperties;jobproperties.LArDigitizationFlags.useEmecIwHighGain.set_Value_and_Lock(False)' 'ESDtoAOD:from TriggerJobOpts.TriggerFlags import TriggerFlags;TriggerFlags.AODEDMSet.set_Value_and_Lock(\"AODSLIM\");' --preInclude HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInlcude.PileUpBunchTrainsMC16c_2017_Config1.py,RunDependentSimData/configLumi_run310000.py --skipEvents=%SKIPEVENTS --autoConfiguration=everything --valid=True --conditionsTag default:OFLCOND-MC16-SDR-25 --geometryVersion=default:ATLAS-R2-2016-01-00-01 --runNumber=312806 --digiSeedOffset1=%RNDM:1 --digiSeedOffset2=%RNDM:1 --digiSteeringConf=StandardSignalOnlyTruth --AMITag=r10724 --steering=doRDO_TRIG --inputHighPtMinbiasHitsFile=%IN_MINH --inputLowPtMinbiasHitsFile=%IN_MINL --numberOfCavernBkg=0 --numberOfHighPtMinBias=0.2595392 --numberOfLowPtMinBias=99.2404608 --pileupFinalBunch=6 --outputAODFile=AOD.pool.root.1 --jobNumber=%RNDM:1 --triggerConfig=RDOtoRDOTrigger=MCRECO:DBF:TRIGGERDBMC:2216,76,260"
      opt_args:
        default: "--outputs AOD.pool.root.1 --nEventsPerFile=5 --nFilesPerJob 2 --athenaTag Athena,21.0.77 --noBuild --expertOnly_skipScout --avoidVP --secondaryDSs IN_MINH:1:mc16_13TeV.361239.Pythia8EvtGen_A3NNPDF23LO_minbias_inelastic_high.simul.HITS.e4981_s3087_s3111/,IN_MINL:1:mc16_13TeV.361238.Pythia8EvtGen_A3NNPDF23LO_minbias_inelastic_low.simul.HITS.e4981_s3087_s3111/ --notExpandSecDSs --forceStaged --forceStagedSecondary"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  deriv:
    run: prun
    in:
      opt_inDS: pile/outDS
      opt_exec:
        default: "Reco_tf.py --inputAODFile=%IN --athenaMPMergeTargetSize 'DAOD_*:0' --maxEvents %MAXEVENTS --preExec 'default:from BTagging.BTaggingFlags import BTaggingFlags;BTaggingFlags.CalibrationTag = \"BTagCalibRUN12-08-49\"; from AthenaCommon.AlgSequence import AlgSequence; topSequence = AlgSequence(); topSequence += CfgMgr.xAODMaker__DynVarFixerAlg(\"InDetTrackParticlesFixer\", Containers = [ \"InDetTrackParticlesAux.\" ] );from AthenaMP.AthenaMPFlags import jobproperties as ampjp;ampjp.AthenaMPFlags.UseSharedWriter=True;import AthenaPoolCnvSvc.AthenaPool;ServiceMgr.AthenaPoolCnvSvc.OutputMetadataContainer=\"MetaData\";topSequence += CfgMgr.xAODMaker__DynVarFixerAlg(\"BTaggingELFixer\", Containers = [\"BTagging_AntiKt4EMTopoAux.\" ] );' --sharedWriter True --skipEvents 0 --runNumber 312806 --AMITag p3992 --passThrough True --outputDAODFile pool.root.1 --reductionConf EXOT27"
      opt_args:
        default: "--outputs DAOD_EXOT27.pool.root.1 --nEventsPerJob 1000 --nEventsPerFile 10 --athenaTag AthDerivation,21.2.79.0 --noBuild --expertOnly_skipScout --avoidVP --forceStaged"
      opt_useAthenaPackages:
        default: true
    out: [outDS]
