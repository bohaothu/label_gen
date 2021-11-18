import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const apiIP="127.0.0.1"
const apiAddr="http://"+apiIP+":5001"

export default new Vuex.Store({
  state: {
    df: {
      fields: [],
      items: [],
      labels: [], // labels_name
      labels_count: []
    },
    tsne: {
      label: [],
      feature: []
    },
    graphFilter: {},
    builtin: {
      isBuiltIn: false,
      dataset: "",
      isClusterLoaded: false
    },
    helper: {
      apiAddr: apiAddr,
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
    resetStateTable(state,payload){
      let tableToBeReset = state[payload.table];
      for(let key in tableToBeReset){
        tableToBeReset[key] = [];
      }
    },
    resetGraphFilter(state, payload){
      state.graphFilter = {};
    },
    updateFilter(state, payload){
      // action, field, id, conditions, name
      if(payload.action === "push"){
        state[payload.field][payload.id] = {conditions: payload.conditions, name: payload.name, id: payload.id};
      }else if(payload.action === "delete"){
        delete state[payload.field][payload.id];
      }
    }
  },
  actions: {
    fetchData(context, payload){
      const requestTable = axios.get(apiAddr+"/random", {params: {row: payload.row_num, features: payload.features_num, labels: payload.labels_num}})
      const requestLabel = axios.get(apiAddr+"/random/label", {params: {labels: payload.labels_num}})
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
      return axios.get(apiAddr+"/builtin/load", {params: {dataset: payload.dataset, nolabel: payload.nolabel, entities: payload.entities}})
      .then((res) => {
        const resLoad = res.data;

        context.commit("addToState", {table: "df", field: "fields", value: resLoad.schema.fields });
        context.commit("addToState", {table: "df", field: "items", value: resLoad.data});
        context.commit("addToState", {table: "df", field: "labels_count", value: resLoad.labels_count});
        context.commit("addToState",{table: "df", field: "labels", value: resLoad.labels_name});

        /*context.commit("addToState", {table: "stat", field: "items", value: helperMethods.transStat(resLoad.stat)});
        context.commit("addToState",{table: "mask", field: "builtInDataset", value: payload.dataset});*/

        context.commit("addToState",{table: "builtin", field: "isBuiltIn", value: true});
        context.commit("addToState",{table: "builtin", field: "dataset", value: payload.dataset});
        context.commit("addToState",{table: "builtin", field: "noLabel", value: payload.nolabel? true:false});

        context.commit("resetStateTable",{table: "tsne"});
        context.commit("resetGraphFilter");

        return {success: true};
      })
      .catch(err => {
        console.error(err);
        return {success: false};
      })
    },
    importDefaultTsne(context,payload){
      const reqTsneLabel = axios.get(apiAddr+"/builtin/tsne", {params: {dataset: payload.dataset, nolabel: payload.nolabel, entities: payload.entities, type: "label"}});
      const reqTsneFeature = axios.get(apiAddr+"/builtin/tsne", {params: {dataset: payload.dataset, nolabel: payload.nolabel, entities: payload.entities, type: "feature"}});
      return axios.all([reqTsneLabel, reqTsneFeature])
      .then(axios.spread((...res) => {
        const resTsneLabel = res[0].data;
        const resTsneFeature = res[1].data;

        context.commit("addToState",{table: "tsne", field: "label", value: resTsneLabel.tsne});
        context.commit("addToState",{table: "tsne", field: "feature", value: resTsneFeature.tsne});

        return {success: true};
      }))
      .catch(err => {
        console.error(err);
        return {success: false};
      })
    },
    noLabelDefaultDataset(context, payload){
      context.commit("addToState",{table: "builtin", field: "noLabel", value: payload.nolabel});
    },
    pushFilter(context, payload){
      context.commit("updateFilter", {action: "push", id: payload.id, field: payload.field, conditions: payload.conditions, name: payload.name});
    },
    deleteFilter(context, payload){
      context.commit("updateFilter", {action: "delete", id: payload.id, field: payload.field});
    }
  },
  modules: {
  }
})
