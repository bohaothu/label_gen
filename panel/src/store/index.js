import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const helperMethods = {
  transStat(obj) {
    let z=[]
    for(let key of Object.keys(obj)){
      z.push({feature_name: key, min: obj[key].min, max: obj[key].max,
      median: obj[key].median, mean: obj[key].mean, std: obj[key].std, var: obj[key].var})
    }
    return z
  }
}

const apiAddr="http://localhost:5000"

export default new Vuex.Store({
  state: {
    df: {
      fields: [],
      items: [],
      labels: [], // labels_name
      labels_count: [],
      suggestion: [],
      tsne: []
    },
    stat: {
      headers: [{text: "Feature", value: "feature_name"}, {text:"最小值", value: "min"},
      {text:"最大值", value: "max"}, {text:"中位数", value: "median"}, {text:"众数", value: "mean"},
      {text:"标准差", value: "std"}, {text:"变异数", value: "var"}],
      items: [{}]
    },
    snackbar: {
      status: false,
      msg: ""
    },
    mask: {
      headers: [],
      labels: [],
      builtInDataset: ""
    },
    builtin: {
      isBuiltIn: false,
      dataset: "",
      noLabel: false
    },
    helper: {
      apiAddr: "http://localhost:5000",
      guid() {
        return  Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      }
    }
  },
  mutations: {
    addToState(state, payload){
      // table: df, field: headers, value: value
      state[payload.table][payload.field] = payload.value
    },
    showSnackbar(state, payload){
      state.snackbar.status = true
      state.snackbar.msg = payload.msg
    },
    RESETMASK(state,payload){
      for(let key in state.mask){
        state.mask[key] = []
      }
    }
  },
  actions: {
    fetchData(context, payload){
      const requestTable=axios.get(apiAddr+"/random", {params: {row: payload.row_num, features: payload.features_num, labels: payload.labels_num}})
      const requestLabel=axios.get(apiAddr+"/random/label", {params: {labels: payload.labels_num}})
      return axios.all([requestTable, requestLabel])
      .then(axios.spread((...res) => {
        const responseTable = res[0].data
        const responseLabel= res[1].data
        context.commit("addToState", {table: "df", field: "fields", value: responseTable.schema.fields })
        context.commit("addToState", {table: "df", field: "items", value: responseTable.data})
        context.commit("addToState", {table: "stat", field: "items", value: helperMethods.transStat(responseTable.stat)})
        context.commit("addToState", {table: "df", field: "labels_count", value: responseTable.labels_count})
        context.commit("addToState",{table: "df", field: "labels", value: responseLabel})
        return true
      })).catch(err => {
        console.error(err)
        return false
      })
    },
    importDefaultDataset(context, payload){
      return axios.get(apiAddr+"/builtin/load", {params: {dataset: payload.dataset, nolabel: payload.nolabel}})
      .then( res => res.data )
      .then( x => {
        context.commit("addToState", {table: "df", field: "fields", value: x.schema.fields });
        context.commit("addToState", {table: "df", field: "items", value: x.data});
        context.commit("addToState", {table: "stat", field: "items", value: helperMethods.transStat(x.stat)});
        context.commit("addToState", {table: "df", field: "labels_count", value: x.labels_count});
        context.commit("addToState",{table: "df", field: "labels", value: x.labels_name});
        context.commit("addToState",{table: "df", field: "tsne", value: x.tsne});
        context.commit("addToState",{table: "mask", field: "builtInDataset", value: payload.dataset});
        context.commit("addToState",{table: "builtin", field: "isBuiltIn", value: true});
        context.commit("addToState",{table: "builtin", field: "dataset", value: payload.dataset});
        context.commit("addToState",{table: "builtin", field: "noLabel", value: false});
        return {success: true}
      })
      .catch(err => {
        console.error(err)
        return {success: false}
      })
    },
    noLabelDefaultDataset(context, payload){
      context.commit("addToState",{table: "builtin", field: "noLabel", value: payload.nolabel});
    },
    importDefaultSuggestion(context, payload){
      let startTime = Date.now()
      return axios.get(apiAddr+"/builtin/predict", {params: {dataset: payload.dataset}})
      .then(res => {
        context.commit("addToState",{table: "df", field: "suggestion", value: res.data})
        return true
      })
      .then(y => {
        let elaspedTime = Date.now() - startTime
        if(y) context.commit("showSnackbar",{msg: "生成推荐成功，用时： "+ elaspedTime + " ms"})
      }).catch(err => {
        console.error(err)
        return false
      })
    },
    fetchFakeSuggestion(context, payload){
      return axios.get(apiAddr+"/random/suggest", {params: {row: payload.row_num, features: payload.features_num, labels: payload.labels_num}})
      .then(res => {
        context.commit("addToState",{table: "df", field: "suggestion", value: res.data})
        return true
      }).catch(err => {
        console.error(err)
        return false
      })
    },
    submitCsv(context, payload){
      let formData = new FormData()
      formData.append("file", payload.csvFile)
      const requestUpload=axios.post(apiAddr+"/upload_csv", formData, {headers: {'Content-Type': 'multipart/form-data'}})
      const requestLabel=axios.get(apiAddr+"/random/label", {params: {labels: payload.labels_num}})

      return axios.all([requestUpload, requestLabel])
      .then(axios.spread((...res) => {
        const responseUpload= JSON.parse(res[0].data.csvResult)
        const responseLabel= res[1].data
        context.commit("addToState", {table: "df", field: "fields", value: responseUpload.schema.fields })
        context.commit("addToState", {table: "df", field: "items", value: responseUpload.data})
        context.commit("addToState", {table: "stat", field: "items", value: helperMethods.transStat(responseUpload.stat)})
        context.commit("addToState", {table: "df", field: "labels_count", value: responseUpload.labels_count})
        context.commit("addToState",{table: "df", field: "labels", value: responseLabel})
        context.commit("showSnackbar",{msg: res[0].data.message})
        return true
      })).catch(err => {
        console.error(err)
        return false
      })
    },
    resetMask(context, payload){
      context.commit("RESETMASK")
    },
    updateMask(context, payload){
      context.commit("addToState", {table: "mask", field: payload.field, value: payload.value})
    }
  },
  modules: {
  }
})
