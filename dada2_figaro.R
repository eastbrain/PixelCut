#!/usr/bin/env Rscript

dada2_func <- function(figaro_out, dir){
  r1_pos <- 0 
  r2_pos <- 0
  lines   <- readLines(figaro_out)
  lineCnt <- 0
  for (line in lines) {
    result <- paste(line,as.character(lineCnt))
    if(lineCnt == 2){
     dat1 <- strsplit(result, split=':')[[1]][2]
     dat2 <- paste(dat1, collapse = " ")
     dat3 <- strsplit(dat2, split = "\\[")[[1]][2]
     dat4 <- strsplit(dat3, split = "\\]")[[1]][1]
     positions <- as.numeric(trimws(strsplit(dat4, split = ",")[[1]]))
     r1_pos <- as.numeric(unlist(strsplit(str_squish(positions), " "))[1])
     r2_pos <- as.numeric(unlist(strsplit(str_squish(positions), " "))[2])
    }
    lineCnt <- lineCnt + 1
  }
  setwd(dir)
  path <- "./data/input"
  fnFs <- sort(list.files(path, pattern="_R1.fastq", full.names = TRUE))
  sample.list <- list.files(path,pattern="_R1.fastq")

  fnRs <- sort(list.files(path, pattern="_R2.fastq", full.names = TRUE))
  sample.names <- sapply(strsplit(basename(fnFs), "_"), `[`, 1)
  filtFs <- file.path(path, "filtered", paste0(sample.names, "_F_filt.fastq.gz"))
  filtRs <- file.path(path, "filtered", paste0(sample.names, "_R_filt.fastq.gz"))
  names(filtFs) <- sample.names
  names(filtRs) <- sample.names
  out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen=c(r1_pos, r2_pos),
   maxN=0, maxEE=c(2,2), truncQ=2, rm.phix=TRUE,
                compress=TRUE, multithread=TRUE)

  errF  <- learnErrors(filtFs, multithread=TRUE)
  errR  <- learnErrors(filtRs, multithread=TRUE)
  dadaFs  <- dada(filtFs, err=errF, multithread=TRUE)
  dadaRs  <- dada(filtRs, err=errR, multithread=TRUE)
  mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose=TRUE)
  seqtab  <- makeSequenceTable(mergers)
  seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)

  Phylum_df <- data.frame(
    Phylum = character(),
    age = numeric(),
    stringsAsFactors = FALSE
  )

  cnt <- 0 
  for(sample in sample.list){
     sample.nm <- strsplit(sample,split='_')[[1]][1]
     seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)
     seqs <- names(seqtab.nochim[sample.nm, ])[seqtab.nochim[sample.nm, ] != 0]
     seq_names     <- paste0("seq", seq(1, length(seqs)))
     fasta_output  <- paste0(">", seq_names, "\n", seqs, "\n",collapse="")
     fasta_file_nm <- paste("figaro.",sample.nm,".fasta",sep="")
     writeLines(fasta_output,fasta_file_nm)
     grep_cmd <- paste('grep -c ">" ',fasta_file_nm,sep="")
     read_cnt <- system(grep_cmd, intern = TRUE)
     taxa     <- assignTaxonomy(seqtab.nochim, "~/together/performance_test/01_figaro/tax/silva_nr99_v138.2_toGenus_trainset.fa.gz", multithread=TRUE)
     Phylum_counts <- as.data.frame(table(taxa[, "Phylum"], useNA = "ifany"))
     colnames(Phylum_counts) <- c("Phylum", sample.nm)
     filenm <- paste(paste("Phylum_ratio.table.",sample.nm,sep=""),".txt",sep="")
     #write.table(Phylum_counts,filenm,sep="\t", col.names=T, row.names=F)

     Class_counts <- as.data.frame(table(taxa[, "Class"], useNA = "ifany"))
     colnames(Class_counts) <- c("Class", sample.nm)
     filenm <- paste(paste("Class_ratio.table.",sample.nm,sep=""),".txt",sep="")
     #write.table(Class_counts,filenm,sep="\t", col.names=T, row.names=F)

     Order_counts <- as.data.frame(table(taxa[, "Order"], useNA = "ifany"))
     colnames(Order_counts) <- c("Order", sample.nm)
     filenm <- paste(paste("Order_ratio.table.",sample.nm,sep=""),".txt",sep="")
     #write.table(Order_counts,filenm,sep="\t", col.names=T, row.names=F)

     Family_counts <- as.data.frame(table(taxa[, "Family"], useNA = "ifany"))
     colnames(Family_counts) <- c("Family", sample.nm)
     filenm <- paste(paste("Family_ratio.table.",sample.nm,sep=""),".txt",sep="")
     #write.table(Family_counts,filenm,sep="\t", col.names=T, row.names=F)

     Genus_counts <- as.data.frame(table(taxa[, "Genus"], useNA = "ifany"))
     filenm <- paste(paste("Family_ratio.table.",sample.nm,sep=""),".txt",sep="")
     colnames(Genus_counts) <- c("Genus", sample.nm)
     filenm <- paste(paste("Genus_ratio.table.",sample.nm,sep=""),".txt",sep="")
     #write.table(Genus_counts,filenm,sep="\t", col.names=T, row.names=F)

     #Species_counts <- as.data.frame(table(taxa[, "Species"], useNA = "ifany"))
     #colnames(Species_counts) <- c("Species", "Count")
     #print(Species_counts)
     #filenm <- paste(paste("Species_ratio.table.","sample.nm",sep=""),".txt",sep="")
     #write.table(Species_counts,filenm,sep="\t", col.names=T, row.names=F)  

     if (cnt == 0) {
      Phylum_df <- Phylum_counts
     }else{
      #Phylum_df <- cbind(Phylum_df,Phylum_counts[,-1])
      Phylum_df <- full_join(Phylum_df,Phylum_counts,by='Phylum')
      colnames(Phylum_df)[ncol(Phylum_df)] <- sample.nm
     }
     if (cnt == 0) {
      Class_df <- Class_counts
     }else{
      #Class_df <- cbind(Class_df,Class_counts[,-1])
      Class_df <- full_join(Class_df,Class_counts,by='Class') 
      colnames(Class_df)[ncol(Class_df)] <- sample.nm
     }
     if (cnt == 0) {
      Order_df <- Order_counts
     }else{
      #Order_df <- cbind(Order_df,Order_counts[,-1])
      Order_df <- full_join(Order_df,Order_counts,by='Order')
      colnames(Order_df)[ncol(Order_df)] <- sample.nm
     }
     if (cnt == 0) {
      Family_df <- Family_counts
     }else{
      #Family_df <- cbind(Family_df,Family_counts[,-1])
      Family_df <- full_join(Family_df,Family_counts,by='Family')
      colnames(Family_df)[ncol(Family_df)] <- sample.nm
     }
     if (cnt == 0) {
      Genus_df <- Genus_counts
     }else{
      #Genus_df <- cbind(Genus_df,Genus_counts[,-1])
      Genus_df <- full_join(Genus_df,Genus_counts,by='Genus')
      colnames(Genus_df)[ncol(Genus_df)] <- sample.nm
     }
     cnt <- cnt + 1
  }
  Phylum_df[is.na(Phylum_df)] <- 0
  Class_df[is.na(Class_df)] <- 0
  Order_df[is.na(Order_df)] <- 0
  Family_df[is.na(Family_df)] <- 0
  Genus_df[is.na(Genus_df)] <- 0

  filenm <- paste(paste("Phylum_count.table","",sep=""),".txt",sep="")
  write.table(Phylum_df,filenm,sep="\t", col.names=T, row.names=F)

  filenm <- paste(paste("Class_count.table","",sep=""),".txt",sep="")
  write.table(Class_df,filenm,sep="\t", col.names=T, row.names=F)

  filenm <- paste(paste("Order_count.table","",sep=""),".txt",sep="")
  write.table(Order_df,filenm,sep="\t", col.names=T, row.names=F)

  filenm <- paste(paste("Family_count.table","",sep=""),".txt",sep="")
  write.table(Family_df,filenm,sep="\t", col.names=T, row.names=F)

  filenm <- paste(paste("Genus_count.table","",sep=""),".txt",sep="")
  write.table(Genus_df,filenm,sep="\t", col.names=T, row.names=F)
}

main <- function() {
  args = commandArgs(trailingOnly=TRUE)
  if (length(args)!=2) {
    #stop("need figaro.output and target.directory\ncreated by Dongin Kim", call.=FALSE)
    print("####################################################################")
    print("usage: Rscript dada2_figaro.R figaro_output_file output_directory", call.=FALSE, call.=FALSE)
    print("")
    print("                                            created by Dongin Kim")
    print("                                                       ISPLab@INU")
    print("                                               gtphrase@inu.ac.kr")
    print("                                                       2025/07/04")
    print("####################################################################")
    return("check the parameter.")
  } 

  library("dada2")
  library("stringr")
  library(dplyr)

  figaro_out <- args[1]
  dir        <- args[2]
  dada2_func(figaro_out,dir)
}
main()
