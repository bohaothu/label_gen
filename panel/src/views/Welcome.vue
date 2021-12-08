<template>
  <div>
    <v-container fluid class="pa-1">
    <v-row dense>
      <v-col cols="12" md="6">
      <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title>
            选择内置数据集
            <v-icon v-if="isFinished.builtIn" class="ml-2" color="green">mdi-check</v-icon>
          </v-card-title>
          <v-card-text>
            <v-row> 
              <v-col><v-select dense :items="builtInDataset" v-model="builtInListSelect" label="数据集"></v-select></v-col>
            </v-row>
          </v-card-text>
          <v-card-action>
            <div class="px-1 d-flex justify-space-between">
              <span class="pt-1 text-subtitle-1">{{ getBuiltInDetail }}</span>
              <v-btn color="primary" @click="importBuiltIn" :loading="isLoading.builtIn" :disabled="!builtInListSelect">导入</v-btn>
            </div>
          </v-card-action>
        </v-card>
      </v-col>
       <v-col cols="12" md="6">
      <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title>
            上传分类器
            <v-icon v-if="isFinished.filter" class="ml-2" color="green">mdi-check</v-icon>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col><v-file-input dense accept="application/json" @change="previewFile" v-model="filterFile"></v-file-input></v-col>
            </v-row>
          </v-card-text>
          <v-card-action>
            <div class="px-1 d-flex justify-space-between">
              <span>&nbsp;</span>
              <v-btn color="primary" @click="readFile" :loading="isLoading.filter" :disabled="!filterFile">导入</v-btn>
            </div>
          </v-card-action>
        </v-card>
      </v-col>
      <v-snackbar v-model="snack.success">{{snack.msg}}</v-snackbar>
    </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Welcome',
  data: () => ({
    defaultDataset: [],
    builtInListSelect: null,
    isLoading: {
      builtIn: false,
      filter: false
    },
    isFinished: {
      builtIn: false,
      filter: false
    },
    snack: {
      msg: "",
      success: false
    },
    filterFile: null // JS File Object
  }),
  mounted() {
    axios.get(this.$store.state.helper.apiAddr+"/available/list")
    .then(res => res.data)
    .then(x => this.defaultDataset = x)
    .catch(err => console.error(err))
  },
  methods: {
    importBuiltIn() {
      if(this.builtInListSelect){
        this.$store.dispatch('importBuiltIn',{dataset: this.builtInListSelect});
        this.isFinished.builtIn = true;
      }else{
        alert("请先选择数据集！")
      }
    },
    previewFile(event){
      console.log(event);
    },
    readFile(){
      if(this.filterFile){
        this.isLoading.filter = true;
        this.filterFile.text()
        .then(file_text => {
          let file_decoded = JSON.parse(file_text);
          return this.$store.dispatch("importUploadFilter", {value: file_decoded.filters})
        })
        .then(x => {
          if(x.success){
            this.isLoading.filter = false;
            this.isFinished.filter = true;
            window.setTimeout(() => {
              this.isFinished.filter = false;
            }, 1000);
          }
        })
      }
      

    }
  },
  computed: {
    builtInDataset() {
      return this.defaultDataset.map(x => x.dataset_name)
    },
    getBuiltInDetail() {
      if(this.defaultDataset.find(x => x.dataset_name === this.builtInListSelect)){
        let detail = this.defaultDataset.find(x => x.dataset_name === this.builtInListSelect);
        return `${detail.features_count} features, ${detail.labels_count} labels`
      }else{
        return ""
      }
    }
  }
}
</script>

<style scoped>
</style>