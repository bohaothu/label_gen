<template>
  <div class="about">
    <v-container fluid>
    <v-row>
      <v-col cols="12" md="6">
      <v-card class="px-4 pb-4 fill-height" elevation="1">
          <v-card-title class="pl-1">
            选择内置数据集
            <v-progress-circular v-if="isLoading.builtIn" class="ml-2" :size="24" indeterminate></v-progress-circular>
            <v-icon v-if="isFinished.builtIn" class="ml-2" color="green">mdi-check</v-icon>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col><v-select :items="builtInDataset" v-model="builtInListSelect" label="数据集"></v-select></v-col>
            </v-row>
          </v-card-text>
          <v-card-action>
            <div class="px-1 d-flex justify-space-between">
              <span class="pt-1 text-subtitle-1">{{ getBuiltInDetail }}</span>
              <v-btn color="primary" @click="importBuiltIn">导入</v-btn>
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
      builtIn: false
    },
    isFinished: {
      builtIn: false
    },
    snack: {
      msg: "",
      success: false
    }
  }),
  mounted() {
    axios.get(this.$store.state.helper.apiAddr+"/builtin/available")
    .then(res => res.data)
    .then(x => this.defaultDataset = x)
    .catch(err => console.error(err))
  },
  methods: {
    importBuiltIn() {
      if(this.builtInListSelect){
        let startTime = Date.now();
        this.isLoading.builtIn = true;
        this.$store.dispatch('importBuiltIn',{dataset: this.builtInListSelect})
        .then(x => {
          if(x.success){
            this.$store.dispatch('importBuiltIn',{dataset: this.builtInListSelect})
            .then(x => {
              if(x.success){
                let elapsedTime = Date.now() - startTime;
                this.snack.msg = "加载 "+this.builtInListSelect+" 成功，用时 "+ elapsedTime + " ms";
                this.snack.success = true;
                this.isLoading.builtIn = false;
                this.isFinished.builtIn = true;
              }
            });
          }
        });
      }else{
        alert("请先选择数据集！")
      }
    }
  },
  computed: {
    builtInDataset() {
      return this.defaultDataset.map(x => x.name)
    },
    getBuiltInDetail() {
      if(this.defaultDataset.find(x => x.name === this.builtInListSelect)){
        let detail = this.defaultDataset.find(x => x.name === this.builtInListSelect);
        return `${detail.instances} instances, ${detail.features} features, ${detail.labels} labels`
      }else{
        return ""
      }
    }
  }
}
</script>

<style scoped>
</style>