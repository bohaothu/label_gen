<template>
  <v-container>
    <v-card style="padding: 0 24px 16px; margin-bottom: 16px;">
      <v-card-title style="padding-left: 0px">上传数据</v-card-title>
      <v-row>
        <v-file-input truncate-length="100" label="训练集" show-size v-model="files"></v-file-input>
      </v-row>
      <v-row>
        <v-file-input truncate-length="100" label="测试集" show-size v-model="files"></v-file-input>
      </v-row>
      <v-card-action>
        <v-btn color="primary" @click="submitCsv">上传</v-btn>
        <span style="font-size: 80%">  支持格式: .zip, .csv</span>
      </v-card-action>
    </v-card>
    <v-card style="padding: 0 24px 16px; margin-bottom: 16px">
      <v-card-title style="padding-left: 0px">生成随机数据</v-card-title>
      <v-row>
        <v-col><v-text-field style="width: 80%" label="数据列数" v-model="row_num"></v-text-field></v-col>
        <v-col><v-text-field style="width: 80%" label="Features 个数" v-model="features_num"></v-text-field></v-col>
        <v-col><v-text-field style="width: 80%" label="Labels 个数" v-model="labels_num"></v-text-field></v-col>
      </v-row>
      <v-card-action>
        <v-btn color="primary" @click="fetchData">生成</v-btn>
      </v-card-action>
    </v-card>
    <v-card style="padding: 0 24px 16px">
      <v-card-title style="padding-left: 0px">选择内置数据集</v-card-title>
      <v-row>
        <v-col><v-select :items="defaultDataset" v-model="builtInListSelect" label="数据集"></v-select></v-col>
      </v-row>
      <v-card-action>
        <v-btn color="primary" @click="importBuiltIn">导入</v-btn>
      </v-card-action>
    </v-card>
    <v-snackbar v-model="snack.success">{{snack.msg}}</v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: "WelcomePage",
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
    builtInListSelect: null
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
        this.$store.dispatch('resetMask')
        this.$store.dispatch('importDefaultDataset',{dataset: this.builtInListSelect})
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
