<template>
  <v-container>
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
    <v-snackbar v-model="success">生成数据成功</v-snackbar>
  </v-container>
</template>
<script>

export default {
  name: "WelcomePage",
  data: () => ({
    row_num: 100,
    features_num: 5,
    labels_num: 10,
    success: false
  }),
  methods: {
    fetchData() {
      this.$store.dispatch('fetchData',{row_num: this.row_num, features_num: this.features_num, labels_num: this.labels_num })
      .then(res => { this.success = res })
    }
  }
}
</script>
