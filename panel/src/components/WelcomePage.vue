<template>
  <v-container>
    <v-card style="padding: 0 24px 16px; margin-bottom: 16px">
      <v-card-title style="padding-left: 0px">上传数据</v-card-title>
      <v-row>
        <v-file-input truncate-length="100" show-size v-model="files"></v-file-input>
      </v-row>
      <v-card-action>
        <v-btn color="primary" @click="submitCsv">上传</v-btn>
      </v-card-action>
    </v-card>
    <v-card style="padding: 0 24px 16px">
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
    <v-snackbar v-model="snack.success">{{snack.msg}}</v-snackbar>
  </v-container>
</template>

<script>

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
    }
  }),
  methods: {
    fetchData() {
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
