import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const helperMethods = {
  transHeader(arr) {
    let z=[]
    let col=""
    for(let item of arr){
      if (item.name === "index"){
        col = "#"
      }else{
        col = item.name
      }
      z.push({text: col, value: item.name, show: true})
    }
    return z
  },
  transStat(obj) {
    let z=[]
    for(let key of Object.keys(obj)){
      z.push({feature_name: key, min: obj[key].min, max: obj[key].max,
      median: obj[key].median, mean: obj[key].mean, std: obj[key].std, var: obj[key].var})
    }
    return z
  }
}

export default new Vuex.Store({
  state: {
    df: {
      headers: [],
      items: [{}],
      labels: [],
      labels_count: []
    },
    stat: {
      headers: [{text: "Feature", value: "feature_name"}, {text:"最小值", value: "min"},
      {text:"最大值", value: "max"}, {text:"中位数", value: "median"}, {text:"众数", value: "mean"},
      {text:"标准差", value: "std"}, {text:"变异数", value: "var"}],
      items: [{}]
    }
  },
  mutations: {
    addToState(state, payload){
      // table: df, field: headers, value: value
      state[payload.table][payload.field] = payload.value
    }
  },
  actions: {
    fetchData(context, payload){
      const requestTable=axios.get("http://localhost:5000/random", {params: {row: payload.row_num, features: payload.features_num, labels: payload.labels_num}})
      const requestLabel=axios.get("http://localhost:5000/random/label", {params: {labels: payload.labels_num}})
      return axios.all([requestTable, requestLabel])
      .then(axios.spread((...res) => {
        const responseTable = res[0].data
        const responseLabel= res[1].data
        context.commit("addToState", {table: "df", field: "headers", value: helperMethods.transHeader(responseTable.schema.fields)})
        context.commit("addToState", {table: "df", field: "items", value: responseTable.data})
        context.commit("addToState", {table: "stat", field: "items", value: helperMethods.transStat(responseTable.stat)})
        context.commit("addToState", {table: "df", field: "labels_count", value: responseTable.labels_count})
        context.commit("addToState",{table: "df", field: "labels", value: responseLabel})
        return true
      })).catch(err => {
        console.error(err)
        return false
      })
    }
  },
  modules: {
  }
})
