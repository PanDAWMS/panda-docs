# https://prodtask-dev.cern.ch/prodtask/inputlist_with_request/42369/

cwlVersion: v1.2
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  seed:
    type: int
    default: 123

outputs:
  outDS_daod:
    type: string
    outputSource: deriv/outDS
  outDS_ntup:
    type: string
    outputSource: ntup_pile/outDS


steps:
  evnt:
    run: prun
    in:
      opt_exec:
        default: "Gen_tf.py --maxEvents=%MAXEVENTS --ecmEnergy=13000 --firstEvent=%FIRSTEVENT:1 --jobConfig=511459 --outputEVNTFile=EVNT.pool.root.1 --randomSeed=%RNDM:%{seed} --runNumber=511459 --AMITag=e8412"
      opt_args:
        default: "--outputs EVNT.pool.root.1 --nEvents=2000 --nJobs 2 --athenaTag AthGeneration,21.6.85 --noBuild --expertOnly_skipScout --avoidVP"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  simul:
    run: prun
    in:
      opt_inDS: evnt/outDS
      opt_exec:
        default: "Sim_tf.py --inputEVNTFile=%IN --maxEvents=%MAXEVENTS --postInclude default:RecJobTransforms/UseFrontier.py --preExec 'EVNTtoHITS:simFlags.SimBarcodeOffset.set_Value_and_Lock(200000)' 'EVNTtoHITS:simFlags.TRTRangeCut=30.0;simFlags.TightMuonStepping=True' --preInclude EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py --skipEvents=%SKIPEVENTS --firstEvent=%FIRSTEVENT:1 --outputHITSFile=HITS.pool.root.1 --physicsList=FTFP_BERT_ATL_VALIDATION --randomSeed=%RNDM:1 --DBRelease=all:current --conditionsTag default:OFLCOND-MC16-SDR-14 --geometryVersion=default:ATLAS-R2-2016-01-00-01_VALIDATION --runNumber=511459 --AMITag=s3126 --DataRunNumber=284500 --simulator=FullG4 --truthStrategy=MC15aPlus"
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
        default: "Reco_tf.py --inputHITSFile=%IN --maxEvents=10 --postExec 'all:CfgMgr.MessageSvc().setError+=[\"HepMcParticleLink\"]' 'ESDtoAOD:fixedAttrib=[s if \"CONTAINER_SPLITLEVEL = '\"'\"'99'\"'\"'\" not in s else \"\" for s in svcMgr.AthenaPoolCnvSvc.PoolAttributes];svcMgr.AthenaPoolCnvSvc.PoolAttributes=fixedAttrib' 'RDOtoRDOTrigger:conddb.addOverride(\"/CALO/Ofl/Noise/PileUpNoiseLumi\",\"CALOOflNoisePileUpNoiseLumi-mc15-mu30-dt25ns\")' 'ESDtoAOD:CILMergeAOD.removeItem(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.LATERAL.LONGITUDINAL.SECOND_R.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_BAD_HV_CELLS.N_BAD_HV_CELLS.ENG_POS.SIGNIFICANCE.CELL_SIGNIFICANCE.CELL_SIG_SAMPLING.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.PTD.BadChannelList\");CILMergeAOD.add(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.N_BAD_CELLS.ENG_BAD_CELLS.BADLARQ_FRAC.AVG_TILE_Q.AVG_LAR_Q.CENTER_MAG.ENG_POS.CENTER_LAMBDA.SECOND_LAMBDA.SECOND_R.ISOLATION.EM_PROBABILITY\");StreamAOD.ItemList=CILMergeAOD()' --postInclude default:PyJobTransforms/UseFrontier.py --preExec 'all:rec.Commissioning.set_Value_and_Lock(True);from AthenaCommon.BeamFlags import jobproperties;jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0);from LArROD.LArRODFlags import larRODFlags;larRODFlags.NumberOfCollisions.set_Value_and_Lock(20);larRODFlags.nSamples.set_Value_and_Lock(4);larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True);larRODFlags.firstSample.set_Value_and_Lock(0);larRODFlags.useHighestGainAutoCorr.set_Value_and_Lock(True)' 'all:from TriggerJobOpts.TriggerFlags import TriggerFlags as TF;TF.run2Config='\"'\"'2016'\"'\"'' 'RAWtoESD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.cutLevel.set_Value_and_Lock(14); from JetRec import JetRecUtils;f=lambda s:[\"xAOD::JetContainer#AntiKt4%sJets\"%(s,),\"xAOD::JetAuxContainer#AntiKt4%sJetsAux.\"%(s,),\"xAOD::EventShape#Kt4%sEventShape\"%(s,),\"xAOD::EventShapeAuxInfo#Kt4%sEventShapeAux.\"%(s,),\"xAOD::EventShape#Kt4%sOriginEventShape\"%(s,),\"xAOD::EventShapeAuxInfo#Kt4%sOriginEventShapeAux.\"%(s,)]; JetRecUtils.retrieveAODList = lambda : f(\"EMPFlow\")+f(\"LCTopo\")+f(\"EMTopo\")+[\"xAOD::EventShape#NeutralParticleFlowIsoCentralEventShape\",\"xAOD::EventShapeAuxInfo#NeutralParticleFlowIsoCentralEventShapeAux.\", \"xAOD::EventShape#NeutralParticleFlowIsoForwardEventShape\",\"xAOD::EventShapeAuxInfo#NeutralParticleFlowIsoForwardEventShapeAux.\", \"xAOD::EventShape#ParticleFlowIsoCentralEventShape\",\"xAOD::EventShapeAuxInfo#ParticleFlowIsoCentralEventShapeAux.\", \"xAOD::EventShape#ParticleFlowIsoForwardEventShape\",\"xAOD::EventShapeAuxInfo#ParticleFlowIsoForwardEventShapeAux.\", \"xAOD::EventShape#TopoClusterIsoCentralEventShape\",\"xAOD::EventShapeAuxInfo#TopoClusterIsoCentralEventShapeAux.\", \"xAOD::EventShape#TopoClusterIsoForwardEventShape\",\"xAOD::EventShapeAuxInfo#TopoClusterIsoForwardEventShapeAux.\",\"xAOD::CaloClusterContainer#EMOriginTopoClusters\",\"xAOD::ShallowAuxContainer#EMOriginTopoClustersAux.\",\"xAOD::CaloClusterContainer#LCOriginTopoClusters\",\"xAOD::ShallowAuxContainer#LCOriginTopoClustersAux.\"]; from eflowRec.eflowRecFlags import jobproperties; jobproperties.eflowRecFlags.useAODReductionClusterMomentList.set_Value_and_Lock(True); from TriggerJobOpts.TriggerFlags import TriggerFlags;TriggerFlags.AODEDMSet.set_Value_and_Lock(\"AODSLIM\");' 'all:from BTagging.BTaggingFlags import BTaggingFlags;BTaggingFlags.btaggingAODList=[\"xAOD::BTaggingContainer#BTagging_AntiKt4EMTopo\",\"xAOD::BTaggingAuxContainer#BTagging_AntiKt4EMTopoAux.\",\"xAOD::BTagVertexContainer#BTagging_AntiKt4EMTopoJFVtx\",\"xAOD::BTagVertexAuxContainer#BTagging_AntiKt4EMTopoJFVtxAux.\",\"xAOD::VertexContainer#BTagging_AntiKt4EMTopoSecVtx\",\"xAOD::VertexAuxContainer#BTagging_AntiKt4EMTopoSecVtxAux.-vxTrackAtVertex\"];' 'ESDtoAOD:from ParticleBuilderOptions.AODFlags import AODFlags; AODFlags.ThinGeantTruth.set_Value_and_Lock(True);  AODFlags.ThinNegativeEnergyCaloClusters.set_Value_and_Lock(True); AODFlags.ThinNegativeEnergyNeutralPFOs.set_Value_and_Lock(True); from JetRec import JetRecUtils; aodlist = JetRecUtils.retrieveAODList(); JetRecUtils.retrieveAODList = lambda : [item for item in aodlist if not \"OriginTopoClusters\" in item];' --preInclude HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_mc16a.py --skipEvents=0 --autoConfiguration=everything --conditionsTag default:OFLCOND-MC16-SDR-16 --geometryVersion=default:ATLAS-R2-2016-01-00-01 --runNumber=511459 --digiSeedOffset1=20 --digiSeedOffset2=20 --digiSteeringConf=StandardSignalOnlyTruth --AMITag=r9364 --steering=doRDO_TRIG --inputHighPtMinbiasHitsFile=%IN_MINH --inputLowPtMinbiasHitsFile=%IN_MINL --numberOfCavernBkg=0 --numberOfHighPtMinBias=0.116075313 --numberOfLowPtMinBias=44.3839246425 --pileupFinalBunch=6 --outputAODFile=AOD.28392797._000020.pool.root.1 --jobNumber=20 --triggerConfig=RDOtoRDOTrigger=MCRECO:DBF:TRIGGERDBMC:2136,35,160"
      opt_args:
        default: "--outputs AOD.pool.root.1 --nEventsPerFile=5 --nFilesPerJob 2 --athenaTag AtlasOffline,21.0.20 --noBuild --expertOnly_skipScout --avoidVP --secondaryDSs IN_MINH:1:mc16_13TeV.361239.Pythia8EvtGen_A3NNPDF23LO_minbias_inelastic_high.simul.HITS.e4981_s3087_s3111/,IN_MINL:1:mc16_13TeV.361238.Pythia8EvtGen_A3NNPDF23LO_minbias_inelastic_low.simul.HITS.e4981_s3087_s3111/ --notExpandSecDSs --forceStaged --forceStagedSecondary"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  deriv:
    run: prun
    in:
      opt_inDS: pile/outDS
      opt_exec:
        default: "Reco_tf.py --inputAODFile=%IN --athenaMPMergeTargetSize 'DAOD_*:0' --maxEvents %MAXEVENTS --preExec 'default:from BTagging.BTaggingFlags import BTaggingFlags;BTaggingFlags.CalibrationTag = \"BTagCalibRUN12-08-49\"; from AthenaCommon.AlgSequence import AlgSequence; topSequence = AlgSequence(); topSequence += CfgMgr.xAODMaker__DynVarFixerAlg(\"InDetTrackParticlesFixer\", Containers = [ \"InDetTrackParticlesAux.\" ] );from AthenaMP.AthenaMPFlags import jobproperties as ampjp;ampjp.AthenaMPFlags.UseSharedWriter=True;import AthenaPoolCnvSvc.AthenaPool;ServiceMgr.AthenaPoolCnvSvc.OutputMetadataContainer=\"MetaData\";topSequence += CfgMgr.xAODMaker__DynVarFixerAlg(\"BTaggingELFixer\", Containers = [\"BTagging_AntiKt4EMTopoAux.\" ] );' --sharedWriter True --skipEvents 0 --runNumber 511459 --AMITag p3992 --passThrough True --outputDAODFile pool.root.1 --reductionConf EXOT27"
      opt_args:
        default: "--outputs DAOD_EXOT27.pool.root.1 --nEventsPerJob 1000 --nEventsPerFile 10 --athenaTag AthDerivation,21.2.79.0 --noBuild --expertOnly_skipScout --avoidVP --forceStaged"
      opt_useAthenaPackages:
        default: true
    out: [outDS]

  ntup_pile:
    run: prun
    in:
      opt_inDS: pile/outDS
      opt_exec:
        default: "PRWConfig_tf.py --inputAODFile=%IN --AMITag=p4108 --outputNTUP_PILEUPFile=NTUP_PILEUP.pool.root.1"
      opt_args:
        default: "--outputs NTUP_PILEUP.pool.root.1 --nEventsPerJob 1000 --nEventsPerFile 10 --athenaTag AthDerivation,21.2.90.0 --noBuild --expertOnly_skipScout --avoidVP --forceStaged"
      opt_useAthenaPackages:
        default: true
    out: [outDS]
    when: $(self.opt_inDS)

