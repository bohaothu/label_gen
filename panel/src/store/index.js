import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const apiIP="127.0.0.1";
const apiAddr=`http://${apiIP}:5001`;


export default new Vuex.Store({
  state: {
    helper: {
      apiAddr: apiAddr,
      guid() {
        return  Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      }
    },
    dataset: "bibtex"
  },
  mutations: {
    addToTable(state, payload){
      // table: df, field: headers, value: value
      state[payload.table] = payload.value;
    },
    pushToTable(state, payload){
      state[payload.table].push(payload.value);
    },
    deleteArrayItemById(state, payload){
      state[payload.table] = state[payload.table].filter(x => x.id !== payload.id);
    },
    editGraphFilter(state, payload){
      state.graphFilter[payload.id] = payload.value;
    }
  },
  actions: {
    importBuiltIn(context, payload){
      context.commit("addToTable",{table: "dataset", value: payload.dataset});
    },
    addGraphFilter(context, payload){
      context.commit("editGraphFilter",{id: payload.id, value: payload.value});
    }
  },
  modules: {
  }
})
