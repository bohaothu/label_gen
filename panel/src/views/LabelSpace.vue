<template>
  <div>
    <v-container fluid>
      <v-row align="center" justify="space-between" style="height: 90vh">
        <v-col cols="12" md="8" class="fill-height d-flex flex-column">
          <v-card outlined class="mx-auto" style="height: 100%; width: 100%;">
            <v-card-text class="fill-height d-flex align-center justify-center rounded">
              <v-progress-circular v-if="!option.series[0].data.length" indeterminate></v-progress-circular>
              <v-chart v-if="option.series[0].data.length" style="height: 100%; width: 100%;" :option="option" autoresize/>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col class="fill-height d-flex flex-column">
          <v-row>
            <v-col cols="6" md="12">
              <v-card outlined class="px-4 pb-4 mx-auto fill-height">
                <v-card-title class="d-flex justify-space-between px-0">
                  Filters
                  <span>
                    <v-btn text color="primary" class="mr-2" @click="reloadWithNoLabel" :disabled="isLoading.noLabel || isFinished.noLabel">
                      <v-icon v-if="!isLoading.noLabel">mdi-backspace</v-icon>
                      <v-progress-circular v-if="isLoading.noLabel" :size="20" indeterminate></v-progress-circular>
                    </v-btn>
                    <v-dialog v-model="toggle.filterDialog" width="960">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="primary" outlined v-bind="attrs" v-on="on">Add Filter</v-btn>
                    </template>
                  <v-card class="px-4 pb-6">
                    <v-card-title class="pl-2 pb-4">Add new filter</v-card-title>
                    <v-card-text class="pl-2">
                      <v-row v-for="(condition, idx) in newFilter" :key="condition.key">
                        <v-col cols="3" class="pb-0">
                          <v-select v-model="condition.field" :items="filterAcceptedMethods.field" style="width: 100%" dense outlined></v-select>
                        </v-col>
                        <v-col cols="3" class="pb-0">
                          <v-select v-model="condition.operator" :items="filterAcceptedMethods.operator[condition.field]" style="width: 100%" dense outlined></v-select>
                        </v-col>
                        <v-col cols="5" class="pb-0">
                          <v-select v-model="condition.value" :items="filterAcceptedMethods.value[condition.field]" style="width: 100%" chips multiple dense outlined></v-select>
                        </v-col>
                        <v-col cols="1" class="pb-0">
                          <v-btn v-if="idx < newFilter.length - 1" color="secondary" @click="removeNewCondition(idx)"><v-icon>mdi-minus</v-icon></v-btn>
                          <v-btn v-if="idx == newFilter.length - 1" color="primary" @click="addNewCondition"><v-icon>mdi-plus</v-icon></v-btn>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-action>
                      <v-btn color="primary" :disabled="checkNewFilterEmptyValues" @click="createFilter">Create Filter</v-btn>
                    </v-card-action>
                  </v-card>
                    </v-dialog>
                  </span>
                </v-card-title>
                <v-card-text class="px-0 pb-0 mb-0" style="overflow-y: scroll; height: 180px">
                  <v-row v-for="(item, idx) in labelFilters" :key="item.key" dense justify="space-between">
                    <v-col cols="10">
                      <v-dialog v-model="toggle.editingDialog" width="960">
                    <template v-slot:activator="{ on, attrs }">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on">
                            <div class="d-flex align-center" style="margin-left: -12px; width:100%; ">
                            <span :style="{'color': getColor(idx),'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.name}} {{getFilterItemCount(item.key)}}</span>
                      </v-tooltip>
                    </template>
                  <v-card class="px-4 pb-2">
                    <v-card-title class="pl-2 pb-4">Edit filter "{{item.name}}"</v-card-title>
                    <v-card-text class="pl-2">
                      <v-row v-for="(condition, idx) in getFilter(item.key)" :key="condition.key">
                        <v-col cols="3" class="pb-0">
                          <v-select v-model="condition.field" :items="filterAllMethods.field" style="width: 100%" dense outlined></v-select>
                        </v-col>
                        <v-col cols="3" class="pb-0">
                          <v-select v-model="condition.operator" :items="filterAllMethods.operator[condition.field]" style="width: 100%" dense outlined></v-select>
                        </v-col>
                        <v-col cols="5" class="pb-0">
                          <v-select v-model="condition.value" :items="filterAllMethods.value[condition.field]" :disabled="!filterAllMethods.value[condition.field]" style="width: 100%" chips multiple dense outlined></v-select>
                        </v-col>
                        <v-col cols="2" class="pb-0">
                          <v-btn v-if="idx < getFilter(item.key).length - 1" color="secondary" @click="removeEditCondition(item.key,idx)"><v-icon>mdi-minus</v-icon></v-btn>
                          <v-btn v-if="idx == getFilter(item.key).length - 1" color="primary" @click="addEditCondition(item.key)"><v-icon>mdi-plus</v-icon></v-btn>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-action>
                      <!--<v-btn color="primary" @click="saveEditedFilter">Save Filter</v-btn>-->
                    </v-card-action>
                  </v-card>
                </v-dialog>
                    </v-col>
                    <v-col cols="2">
                      <v-btn small text @click="removeFilter(idx)"><v-icon>mdi-delete-forever</v-icon></v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-card-actions class="justify-center" style="position: absolute; left: 50%; top: 88%; transform: translate(-50%,-50%);">
              </v-card-actions>
            </v-card></v-col>
            <v-col cols="6" md="12">
              <v-card outlined class="px-4 pb-4 mx-auto fill-height" style="width: 100%">
                <v-card-title class="px-0">Filtered Results</v-card-title>
                <v-card-text class="px-0" style="text-align: justify">
                  <div style="text-align: justify" v-html="getCurrentPoint"></div>
                  <!-- <p v-for="(item, idx) in searchData" :key="item.key" dense>
                    {{ item.filter.name }} {{ item.filterResult.length }}
                  </p> -->
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { ScatterChart } from "echarts/charts";
import { TitleComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import axios from 'axios';

use([
  CanvasRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

export default {
  name: 'LabelSpace',
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "light"
  },
  mounted() {
    this.option.series[0].data = new Array();
    this.option.series[0].data = this.$store.state.df.tsne;
    this.newFilter = [{ field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()}];
    if(this.$store.state.builtin.isBuiltIn){
      let requestUrl = "";
      if(this.$store.state.builtin.noLabel){
        requestUrl = [this.$store.state.helper.apiAddr,"/builtin/cluster?dataset=",this.$store.state.builtin.dataset,"&nolabel=1"].join("");
      }else{
        requestUrl = [this.$store.state.helper.apiAddr,"/builtin/cluster?dataset=",this.$store.state.builtin.dataset].join("");
      };
      axios.get(requestUrl)
      .then(res => res.data)
      .then(x => {
        const clusterResult = x.cluster_result;
        for(let [idx,item] of clusterResult.entries()){
          let filter_id = this.$store.state.helper.guid();
          let filter_name = "Cluster " + idx;
          let clusterCondition = [{field: "Cluster", operator: "Kmeans", value: item, key: this.$store.state.helper.guid()}];
          this.labelFilters.push({name: filter_name, conditions: clusterCondition, key: filter_id});
          let wanted_tsne_points = [];
          item.forEach( x => {
            let new_point = this.$store.state.df.tsne[x];
            new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
            wanted_tsne_points.push(new_point);
            if(this.labelFilterNames[x]){
              if(!this.labelFilterNames[x].map(y => y.name).includes(filter_name)){
                this.labelFilterNames[x].push({name: filter_name, filter_id: filter_id});
              }
            }else{
              this.labelFilterNames[x] = [{name: filter_name, filter_id: filter_id}];
            }
            } );
          this.option.series.push({name: filter_name, type: "scatter", data: wanted_tsne_points, filter_key: filter_id});
          this.option.legend.data.push(filter_name);
        }
      })
      .catch(err => console.error(err))
    }
    //console.log(this.searchData)
  },
  data() {
    return {
      toggle: {
        filterDialog: false,
        editorDialog: false
      },
      isLoading: {
        noLabel: false
      },
      isFinished: {
        noLabel: false
      },
      filterAcceptedMethods: {
        field: ["Labels"],
        operator: { Labels: ["Contain","Not Contain"] },
        value: { Labels: this.$store.state.df.labels }
      },
      filterAllMethods: {
        field: ["Labels","Cluster"],
        operator: { Labels: ["Contain","Not Contain"], Cluster: ["Kmeans"] },
        value: { Labels: this.$store.state.df.labels, Cluster: false }
      },
      newFilter:[],
      labelFilters: [],
      labelFilterNames: [], // array of array, represent filter name of each data points
      option: {
        xAxis: {
          type: "value"
        },
        yAxis: {
          type: "value"
        },
        legend: {
          data: []
        },
        tooltip: {
          trigger: "item",
          position: "top",
          formatter: (params) => {
            const filter_of_data = this.getFilterNames(params.data[2].df_index);
            const label_of_data = this.genLabelArr(params.data[2].df_index);
            this.currentPoint = params.data[2].df_index;
            let tooltip_html="";
            if(filter_of_data.length){
              tooltip_html="Groups (NUM): </br>".replace("NUM",filter_of_data.length);
              for(let item of filter_of_data){
                tooltip_html += this.getTooltipBull(item.filter_id) + item.name + "</br>";
              }
            }
            if(label_of_data.length){
              tooltip_html += "Labels (NUM): </br>".replace("NUM",label_of_data.length);
              for(let item of label_of_data){
                tooltip_html += this.getTooltipBull(-1) + item.name.replace("\\","") + "</br>";
              }
            }else{
              tooltip_html += "No Labels";
            }
            return tooltip_html;
          }
        },
        series: [
          {
            symbolSize: 10,
            data: [],
            type: "scatter"
          }
        ],
        color:  ['#bbb','#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0']
      },
      currentPoint: -1
    }
  },
  methods: {
    removeNewCondition(index){
      const key_to_remove = this.newFilter[index].key;
      this.newFilter = this.newFilter.filter(x => x.key != key_to_remove)
    },
    addNewCondition() {
      this.newFilter.push({ field: "", operator: "", value: [], key: this.$store.state.helper.guid()});
    },
    removeEditCondition(key,index){
      const filter_index_to_edit = this.labelFilters.findIndex(x => x.key === key);
      const filter_to_edit = this.labelFilters[filter_index_to_edit].conditions;
      const key_to_remove = filter_to_edit[index].key;
      this.labelFilters[filter_index_to_edit].conditions = this.labelFilters[filter_index_to_edit].conditions.filter(x => x.key !== key_to_remove);
    },
    addEditCondition(key) {
      const filter_to_edit = this.labelFilters.filter(x => x.key === key)[0].conditions;
      filter_to_edit.push({field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()});
    },
    createFilter() {
      // push filter to labelFilters array
      const filter_id = this.$store.state.helper.guid()
      const filter_name = this.newFilter[0].operator + " \"" + this.newFilter[0].value[0] + "\"" + (this.newFilter[0].value.length > 1? " and "+ (this.newFilter[0].value.length -1) + " more":"")
      this.labelFilters.push({name: filter_name, conditions: this.newFilter, key: filter_id});
      //reset new filter
      this.newFilter = [{ field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()}];
      this.toggle.filterDialog = false;
      //add new point to chart
      let wanted_tsne_points = [];
      console.log(this.searchData[this.labelFilters.length - 1].filterResult);
      console.log("I am here2")
      this.searchData[this.labelFilters.length - 1].filterResult.forEach( x => {
        let new_point = this.$store.state.df.tsne[x];
        new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
        wanted_tsne_points.push(new_point);
        if(this.labelFilterNames[x]){
            if(!this.labelFilterNames[x].map(y => y.name).includes(filter_name)){
              this.labelFilterNames[x].push({name: filter_name, filter_id: filter_id});
            }
          }else{
            this.labelFilterNames[x] = [{name: filter_name, filter_id: filter_id}];
          }
        } );
      //console.log(wanted_tsne_points);
      const next_chart_idx = this.option.series.findIndex(x => x.filter_key === "toberemove");
      //console.log(next_chart_idx);
      if(next_chart_idx !== -1){
        this.option.series[next_chart_idx].data = wanted_tsne_points;
        this.option.series[next_chart_idx].filter_key = filter_id;
        this.option.legend.data.push(filter_name);
        console.log(this.option.legend);
      }else{
        this.option.series.push({name: filter_name, type: "scatter", data: [wanted_tsne_points], filter_key: filter_id});
      }
    },
    removeFilter(index) {
      const key_to_remove = this.labelFilters[index].key;
      const chart_idx_to_remove = this.option.series.findIndex(x => x.filter_key === key_to_remove);
      // remove filter legend
      this.option.legend.data = this.option.legend.data.filter(x => x != this.labelFilters[index].name);
      // remove filter result from chart
      this.option.series[chart_idx_to_remove].data = [];
      this.option.series[chart_idx_to_remove].filter_key = "toberemove";
      // remove filter
      this.labelFilters = this.labelFilters.filter(x => x.key !== key_to_remove);
    },
    genLabelArr(df_index){
      const labels_in_entity = this.$store.state.df.items[df_index].labels;
      const labelArr = [];
      for(let [i,v] of labels_in_entity.entries()){
        v > 0? labelArr.push({name: this.$store.state.df.labels[i], label_index: i}):void(0);
      }
      return labelArr;
    },
    reloadWithNoLabel() {
      if(this.$store.state.builtin.isBuiltIn){
        this.isLoading.noLabel = true;
        this.$store.dispatch('importDefaultDataset',{dataset: this.$store.state.builtin.dataset, nolabel: 1})
        .then(x => {
          if(x.success){
            axios.get([this.$store.state.helper.apiAddr,"/builtin/cluster?dataset=",this.$store.state.builtin.dataset,"&nolabel=1"].join(""))
            .then(res => res.data)
            .then(x => {
              const seriesLength = JSON.parse(JSON.stringify(this.option.series.length));
              for(let i=1; i<seriesLength; i++){
                this.option.series.pop();
              }
              this.option.series[0].data=[];
              this.option.series[0].data = this.$store.state.df.tsne;
              this.labelFilters = [];
              this.labelFilterNames = [];
              this.newFilter = [{ field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()}];
              const clusterResult = x.cluster_result;
              for(let [idx,item] of clusterResult.entries()){
                let filter_id = this.$store.state.helper.guid();
                let filter_name = "Cluster " + idx;
                let clusterCondition = [{field: "Cluster", operator: "Kmeans", value: item, key: this.$store.state.helper.guid()}];
                this.labelFilters.push({name: filter_name, conditions: clusterCondition, key: filter_id});
                let wanted_tsne_points = [];
                item.forEach( x => {
                  let new_point = this.$store.state.df.tsne[x];
                  new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
                  wanted_tsne_points.push(new_point);
                  if(this.labelFilterNames[x]){
                    if(!this.labelFilterNames[x].map(y => y.name).includes(filter_name)){
                      this.labelFilterNames[x].push({name: filter_name, filter_id: filter_id});
                    }
                  }else{
                    this.labelFilterNames[x] = [{name: filter_name, filter_id: filter_id}];
                  }
                  } );
                this.option.series.push({name: filter_name, type: "scatter", data: wanted_tsne_points, filter_key: filter_id});
                this.option.legend.data.push(filter_name);
                this.isLoading.noLabel = false;
                this.isFinished.noLabel = true;
                this.$store.dispatch('noLabelDefaultDataset',{nolabel: true});
              }
            })
            .catch(err => console.error(err))
          }
        })
        .catch(err => console.error(err));
      }
    }
  },
  computed: {
    getCurrentPoint(){
      if(this.currentPoint >= 0){
        const current_item = this.$store.state.df.items[this.currentPoint];
        const excluded_keys = ["index","labels"];
        const keys = Object.keys(current_item).filter(x => !excluded_keys.includes(x)).slice(0,10);
        let currentPoint_html = "";
        for(let item of keys){
          currentPoint_html += `<h5 style="display: inline">${item}</h5> ${current_item[item]}</br>`;
        }
        return currentPoint_html;
      }
    },
    getColor() {
      return function(index){
        const key_to_find = this.labelFilters[index].key;
        const chart_idx_to_find = this.option.series.findIndex(x => x.filter_key === key_to_find);
        return this.option.color[chart_idx_to_find];
      }
    },
    getTooltipBull(){
      return function(key){
        const chart_idx_to_find = this.option.series.findIndex(x => x.filter_key === key);
        return `<span style="color: ${this.option.color[chart_idx_to_find]}; font-size: 1rem">&bull;&nbsp;</span>`
      }
    },
    getFilter() {
      return function(key){
        return this.labelFilters.filter(x => x.key === key)[0].conditions;
      };
    },
    getFilterNames(){
      return function(idx){
          return this.labelFilterNames[idx].filter(x => this.labelFilters.map(y => y.key).includes(x.filter_id));
      };
    },
    getFilterItemCount(){
      return function(filter_key){
        const current_filter = this.option.series.filter(x => x.filter_key === filter_key);
        if(current_filter.length){
          return "(" + current_filter[0].data.length + ")";
        }
      }
    },
    checkNewFilterEmptyValues(){
      return this.newFilter.every(x => x.value.length === 0)
    },
    searchData() {
      let z=[];
      const that = this;
      const filterMethod = {
        Labels: {
          Contain(val) {
            let wanted_item = [];
            for(let label of val){
              let label_index = that.$store.state.df.labels.indexOf(label);
              console.log(label_index);
              that.$store.state.df.items.filter(x => x.labels[label_index] === 1)
              .forEach(y => wanted_item.includes(y.index)? void(0):wanted_item.push(y.index));
            }
            return wanted_item;
          },
          NotContain(val) {
            let wanted_item = [];
            //let wanted_tsne_points = [];
            for(let label of val){
              let label_index = that.$store.state.df.labels.indexOf(label);
              that.$store.state.df.items.filter(x => x.labels[label_index] === 0)
              .forEach(y => wanted_item.includes(y.index)? void(0):wanted_item.push(y.index));
              //wanted_item.forEach(wanted_tsne_points.push(this.$store.state.df));
            }
            return wanted_item;
          }
        },
        Cluster: {
          Kmeans(val){
            return val;
          }
        }
      };
      console.log("searchData start");
      for(let filter of this.labelFilters){
        let wanted_index=[];
        for(let condition of filter.conditions){
          //console.log(filterMethod[condition.field][condition.operator.replace(/\s/g, '')](condition.value))
          filterMethod[condition.field][condition.operator.replace(/\s/g, '')](condition.value)
          .forEach(y => wanted_index.includes(y)? void(0):wanted_index.push(y));
        }
        z.push({filter: filter, filterResult: wanted_index, key: this.$store.state.helper.guid()});
      }
      console.log(z);
      return z;
    }
  }
}
</script>

<style scoped>
</style>