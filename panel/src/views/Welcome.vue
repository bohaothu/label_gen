<template>
  <div class="about">
    <v-container fluid>
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title class="pl-0">上传数据</v-card-title>
          <v-card-text><v-row>
            <v-col cols="6"><v-file-input truncate-length="100" label="训练集" show-size v-model="files"></v-file-input></v-col>
            <v-col cols="6"><v-file-input truncate-length="100" label="测试集" show-size v-model="files"></v-file-input></v-col>
          </v-row></v-card-text>
          <v-card-action>
            <v-btn color="primary" @click="submitCsv">上传</v-btn>
            <span style="margin-left: 16px; font-size: 80%">支持格式: .zip, .csv</span>
          </v-card-action>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title class="pl-0">生成随机数据</v-card-title>
          <v-card-text><v-row>
            <v-col cols="4"><v-text-field label="数据列数" v-model="row_num"></v-text-field></v-col>
            <v-col cols="4"><v-text-field label="Features 个数" v-model="features_num"></v-text-field></v-col>
            <v-col cols="4"><v-text-field label="Labels 个数" v-model="labels_num"></v-text-field></v-col>
          </v-row></v-card-text>
          <v-card-action>
            <v-btn color="primary" @click="fetchData">生成</v-btn>
          </v-card-action>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
      <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title class="pl-0">
            选择内置数据集
            <v-progress-circular v-if="isLoading.builtIn" class="ml-2" :size="24" indeterminate></v-progress-circular>
            <v-icon v-if="isFinished.builtIn" class="ml-2" color="green">mdi-check</v-icon>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col><v-select :items="defaultDataset" v-model="builtInListSelect" label="数据集"></v-select></v-col>
            </v-row>
          </v-card-text>
          <v-card-action>
            <v-btn color="primary" @click="importBuiltIn">导入</v-btn>
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
    row_num: 100,
    features_num: 5,
    labels_num: 10,
    files: null,
    snack: {
      success: false,
      msg: ""
    },
    defaultDataset: [],
    builtInListSelect: null,
    isLoading: {
      builtIn: false
    },
    isFinished: {
      builtIn: false
    }
  }),
  mounted() {
    axios.get("http://localhost:5000/builtin/list")
    .then(res => res.data)
    .then(x => this.defaultDataset = x)
    .catch(err => console.error(err))
  },
  methods: {
    fetchData() {
      this.$store.dispatch('resetMask')
      this.$store.dispatch('fetchData',{row_num: this.row_num, features_num: this.features_num, labels_num: this.labels_num })
      .then(res => {
        this.snack.success = res
        this.snack.msg = res? "生成数据成功":"未知错误"
        })
      this.$store.dispatch('fetchFakeSuggestion',{row_num: this.row_num, features_num: this.features_num, labels_num: this.labels_num })
      .then(res => {
        this.snack.success = res
        this.snack.msg = res? "生成推荐成功":"未知错误"
        })
    },
    importBuiltIn() {
      if(this.builtInListSelect){
        let startTime = Date.now();
        this.isLoading.builtIn = true;
        this.$store.dispatch('resetMask');
        this.$store.dispatch('importDefaultDataset',{dataset: this.builtInListSelect, nolabel: 0})
        .then(x => {
          if(x.success){
            let elaspedTime = Date.now() - startTime;
            this.isLoading.builtIn = false;
            this.snack.success = this.$store.state.df.items.length? true:false;
            this.snack.msg = "载入 "+this.builtInListSelect+" 成功，用时 "+ elaspedTime + " ms";
            this.isFinished.builtIn = true;
          }
        });
      }else{
        alert("请先选择数据集！")
      }
    },
    submitCsv() {
      if(this.files){
        this.$store.dispatch('submitCsv', {csvFile: this.files, labels_num: 30 })
        .then(res => {
          this.snack.success = res
          this.snack.msg = res? "生成数据成功":"未知错误"
        })
      }
    }
  }
}
</script>

<style scoped>
</style>