import logging
import scanpy as sc
import torch
import warnings
import argparse
import GSG
import warnings
warnings.filterwarnings("ignore")

def build_args():
    parser = argparse.ArgumentParser(description="GAT")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0])
    parser.add_argument("--device", type=int, default=-1)
    parser.add_argument("--warmup_steps", type=int, default=-1)
    parser.add_argument("--num_heads", type=int, default=4,
                        help="number of hidden attention heads")
    parser.add_argument("--num_out_heads", type=int, default=1,
                        help="number of output attention heads")
    parser.add_argument("--residual", action="store_true", default=False,
                        help="use residual connection")
    parser.add_argument("--in_drop", type=float, default=0.2,
                        help="input feature dropout")
    parser.add_argument("--attn_drop", type=float, default=0.1,
                        help="attention dropout")
    parser.add_argument("--weight_decay", type=float, default=2e-4,
                        help="weight decay")
    parser.add_argument("--negative_slope", type=float, default=0.2,
                        help="the negative slope of leaky relu for GAT")
    parser.add_argument("--drop_edge_rate", type=float, default=0.0)
    parser.add_argument("--optimizer", type=str, default="adam")
    parser.add_argument("--max_epoch_f", type=int, default=300)
    parser.add_argument("--lr_f", type=float, default=0.01, help="learning rate for evaluation")
    parser.add_argument("--weight_decay_f", type=float, default=1e-4, help="weight decay for evaluation")
    parser.add_argument("--linear_prob", action="store_true", default=True)
    parser.add_argument("--load_model", action="store_true")
    parser.add_argument("--save_model", action="store_true")
    parser.add_argument("--use_cfg", action="store_true")
    parser.add_argument("--logging", action="store_true")
    parser.add_argument("--scheduler", action="store_true", default=True)
    parser.add_argument("--concat_hidden", action="store_true", default=False)

    # for graph classification
    parser.add_argument("--pooling", type=str, default="mean")
    parser.add_argument("--deg4feat", action="store_true", default=False, help="use node degree as input feature")
    parser.add_argument("--batch_size", type=int, default=32)

    # adjustable parameters
    parser.add_argument("--mask_rate", type=float, default=0.8)
    parser.add_argument("--encoder", type=str, default="gin")
    parser.add_argument("--decoder", type=str, default="gin")
    parser.add_argument("--num_hidden", type=int, default=128,
                        help="number of hidden units")
    parser.add_argument("--num_layers", type=int, default=3,
                        help="number of hidden layers")
    parser.add_argument("--activation", type=str, default="elu")
    parser.add_argument("--max_epoch", type=int, default=500,
                        help="number of training epochs")
    parser.add_argument("--lr", type=float, default=0.001 , 
                        help="learning rate")
    parser.add_argument("--alpha_l", type=float, default=4, help="`pow`inddex for `sce` loss")
    parser.add_argument("--loss_fn", type=str, default="sce")
    parser.add_argument("--replace_rate", type=float, default=0.05)
    parser.add_argument("--norm", type=str, default="batchnorm")

    # GSG parameter
    parser.add_argument("--feature_dim_method", type=str, default="PCA")
    parser.add_argument("--num_features", type=int, default=600)
    parser.add_argument("--threshold_radius", type=int, default=25)
    parser.add_argument("--folder_name", type=str, default="data/10X/")
    parser.add_argument("--sample_name", type=str, default="151673")
    parser.add_argument("--cluster_label", type=str, default= "")
    parser.add_argument("--num_classes", type=int, default=7,help = "The number of clusters")

    # read parameters
    args = parser.parse_args()
    return args

def main(args):
    # make new folder
    result_file = args.folder_name  +  args.sample_name 
    GSG.mkdir(result_file)
    adata = GSG.read_10X_Visium_with_label(result_file)
    if(args.cluster_label == ""):
        num_classes = args.num_classes
    else:
        num_classes = adata.obs[args.cluster_label].nunique()

    # graph construction
    adata,graph = GSG.Graph_10X(adata,args)

    # train model and embedding in adata.obsm["GSG_embedding"]
    adata,model = GSG.GSG_train(adata,graph,args)

    # kmeans cluster and result of clusters saved in adata.obs["GSG_Kmeans_cluster"]
    adata.obs["GSG_Kmeans_cluster"] = GSG.KMeans_use(adata.obsm["GSG_embedding"],num_classes)
    adata.obs["GSG_Kmeans_cluster_str"] = adata.obs["GSG_Kmeans_cluster"].astype(str)

    # UMAP
    sc.pp.neighbors(adata, n_neighbors=10,use_rep='GSG_embedding')
    sc.tl.umap(adata)
    fig_new = sc.pl.umap(adata, color="GSG_Kmeans_cluster_str",title ="GSG_Cluster_UMAP",size = 50,return_fig=True)
    fig_new.savefig(result_file + "/GSG_Cluster_UMAP.pdf",bbox_inches='tight',dpi =1000)

    # spatial picture
    adata = GSG.GSG_Spatial_Pic(adata,args,result_file)

    # save data and model
    if args.save_model:
        logging.info("Saveing Model ...")
        torch.save(model.state_dict(), result_file + "/" + args.sample_nam + "_saved_model.pt")
    adata.write(result_file + "/" + args.sample_name + ".h5ad")

if __name__ == "__main__":
    args = build_args()
    print(args)
    main(args)
