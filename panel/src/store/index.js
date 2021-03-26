import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    df: {
      headers: [{text: null, value: null, show: true}],
      items: [{}],
      labels: []
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
  },
  modules: {
  }
})
