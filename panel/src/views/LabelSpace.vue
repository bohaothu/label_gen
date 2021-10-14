<template>
  <div>
    <v-container fluid>
      <v-row align="center" justify="space-between" style="height: 90vh">
        <v-col cols="12" md="8" class="fill-height d-flex flex-column">
          <v-card outlined class="mx-auto" style="height: 100%; width: 100%;">
            <v-card-text class="fill-height d-flex flex-column align-center justify-center rounded">
              <v-progress-circular v-if="!options[spaceTab].series[0].data.length" indeterminate></v-progress-circular>
              <v-chart v-if="options[spaceTab].series[0].data.length" style="height: 100%; width: 100%;" :option="options[spaceTab]" autoresize/>
              <v-btn-toggle v-if="options[spaceTab].series[0].data.length" v-model="spaceTab" @change="spaceTabOnChange">
                <v-btn v-for="item in spaceTabs" :key="item.tab">
                  <v-icon small left>{{ item.icon }}</v-icon> {{ item.tab }}
                </v-btn>
              </v-btn-toggle>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col class="fill-height d-flex flex-column">
          <v-row>
            <v-col cols="6" md="12">
              <v-card outlined class="px-4 pb-4 mx-auto fill-height">
                <v-card-title class="d-flex justify-space-between px-0">
                  <span>
                  <v-menu bottom :close-on-click="true" :close-on-content-click="false" v-model="toggle.quickFilterMenu">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn v-bind="attrs" v-on="on" class="mr-2" text>Graph Filters</v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="mb-0">Create Graph Filter</v-card-title>
                      <v-card-subtitle class="py-0">建立过滤器，在可视化图中将符合过滤条件的点标出</v-card-subtitle>
                      <v-card-text class="pa-0">
                        <v-list class="py-0">
                          <v-list-item class="py-0">
                            <v-list-item-content class="py-0">
                              <v-list-item-title>Labels contain</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item class="py-0">
                            <!--<v-list-item-title class="mb-0">Labels contain</v-list-item-title>-->
                            <v-list-item-content class="py-0">
                              <v-chip-group column multiple active-class="primary--text" v-model="quickFilter">
                                <v-chip v-for="(item,idx) in this.$store.state.df.labels" :key="'graph'+idx">{{item}}</v-chip>
                              </v-chip-group>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text @click="toggle.quickFilterMenu = false">Cancel</v-btn>
                        <v-btn color="primary" text @click="quickCreateFilter">Create</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-menu>
                  </span>
                  <span>
                  <v-menu bottom :close-on-click="true" :close-on-content-click="false" v-model="toggle.entityFilterMenu">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn dark color="indigo" class="mr-2" v-bind="attrs" v-on="on">
                        <v-icon>mdi-filter</v-icon>
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="mb-0">Create Entities Filter</v-card-title>
                      <v-card-subtitle class="py-0">设定过滤条件，在可视化图中保留符合条件的点</v-card-subtitle>
                      <v-card-text class="pa-0">
                        <v-list class="py-0">
                          <v-list-item class="py-0">
                            <v-list-item-content class="py-0">
                              <v-list-item-title>Labels contain</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item class="py-0">
                            <v-list-item-content class="py-0">
                              <v-chip-group column multiple active-class="primary--text" v-model="entityFilter">
                                <v-chip v-for="(item,idx) in this.$store.state.df.labels" :key="'entity'+idx">{{item}}</v-chip>
                              </v-chip-group>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn text @click="toggle.entityFilterMenu = false">Cancel</v-btn>
                        <v-btn text color="primary" @click="performEntityFilter">Perform</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-menu>
                    <!--
                    <v-btn text color="primary" class="mr-2" @click="reloadWithNoLabel" :disabled="isLoading.noLabel || isFinished.noLabel">
                      <v-icon v-if="!isLoading.noLabel">mdi-backspace</v-icon>
                      <v-progress-circular v-if="isLoading.noLabel" :size="20" indeterminate></v-progress-circular>
                    </v-btn>
                    -->
                  </span>
                </v-card-title>
                <v-card-text class="px-0 pb-0 mb-0 fill-height">
                  <v-row v-for="(item, idx) in labelFilters" :key="item.key" dense justify="space-between">
                    <v-col cols="10">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on" @click="toggle.editorDialog = true">
                            <div class="d-flex align-center" style="margin-left: -12px; width:100%; ">
                            <span :style="{'color': getColor(idx),'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.name}} {{getFilterItemCount(item.key)}}</span>
                      </v-tooltip>
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
                <v-card-title class="px-0">
                  <v-btn @click="chartDebug" text>Details</v-btn>
                </v-card-title>
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
    <v-snackbar v-model="snackbar.success">{{snackbar.msg}}</v-snackbar>
    <v-dialog v-model="this.toggle.clusterDialog" persistent max-width="320">
      <v-card>
        <v-card-title class="text-h5">
          加载聚类结果？
        </v-card-title>
        <v-card-text>
          <span>数据集 <b>{{this.$store.state.builtin.dataset}}</b></span> <br>
          <span>聚类算法 <b>Kmeans (默认)</b></span> <br>
          <span>聚类个数 <b>4 (默认)</b></span>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="toggle.clusterDialog = false;">
            Disagree
          </v-btn>
          <v-btn color="green darken-1" text @click="loadCluster">
            Agree
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import { GridComponent, LegendComponent, TitleComponent, TooltipComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import axios from 'axios';

use([
  BarChart,
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
  created() {
    if(this.$store.state.builtin.isBuiltIn){
      this.toggle.clusterDialog = true;
    }
  },
  mounted() {
    for(let i=0; i<this.spaceTabs.length; i++){
      this.options[i].series[0].data = new Array();
      this.options[i].series[0].data = this.$store.state.tsne[this.spaceTabs[i].tsne_type];
    }
    this.newFilter = [{ field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()}];
  },
  data() {
    return {
      toggle: {
        filterDialog: false,
        editorDialog: false,
        quickFilterMenu: false,
        entityFilterMenu: false,
        clusterDialog: false
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
      labelFilters: [],
      labelFilterNames: [], // array of array, represent filter name of each data points
      formData: {
        figureField: "",
        figureType: ""
      },
      dialogChartOptions: {
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [120, 200, 150, 80, 70, 110, 130],
          type: 'bar'
        }]
      },
      options: [{
        xAxis: {
          type: "value"
        },
        yAxis: {
          type: "value"
        },
        legend: {
          y: "top",
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
      {
        xAxis: {
          type: "value"
        },
        yAxis: {
          type: "value"
        },
        legend: {
          y: "top",
          data: []
        },
        series: [
          {
            symbolSize: 10,
            data: [],
            type: "scatter"
          }
        ],
        color:  ['#bbb','#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0']
      }],
      currentPoint: -1,
      spaceTab: 0,
      spaceTabs: [
        { tab: "Label Space", icon: "mdi-tag", tsne_type: "label"},
        { tab: "Feature Space", icon: "mdi-pound", tsne_type: "feature"}
      ],
      quickFilter: [],
      entityFilter: [],
      snackbar: {
        success: false,
        msg: ""
      }
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
    quickCreateFilter() {
      // push filter to labelFilters array
      //console.log(this.quickFilter)
      let quickFilterValue = [];
      for(let item of this.quickFilter){
        quickFilterValue.push(this.$store.state.df.labels[item]);
      }
      let newQuickFilter = [{field: "Labels", operator: "Contain", key: this.$store.state.helper.guid(), value: quickFilterValue}];
      let filter_id = this.$store.state.helper.guid();
      let filter_name = newQuickFilter[0].operator + " \"" + newQuickFilter[0].value[0] + "\"" + (newQuickFilter[0].value.length > 1? " and "+ (newQuickFilter[0].value.length -1) + " more":"");
      this.labelFilters.push({name: filter_name, conditions: newQuickFilter, key: filter_id});
      //console.log("labelFilters",this.labelFilters);
      for(let i=0; i<this.spaceTabs.length; i++){
        //add new point to chart
        let wanted_tsne_points = [];
        console.log("filterResult",this.searchData[this.labelFilters.length - 1].filterResult);
        this.searchData[this.labelFilters.length - 1].filterResult.forEach( x => {
          let new_point = this.$store.state.tsne[this.spaceTabs[i].tsne_type][x];
          new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
          wanted_tsne_points.push(new_point);
          if(this.labelFilterNames[x]){
              if(!this.labelFilterNames[x].map(y => y.name).includes(filter_name)){
                this.labelFilterNames[x].push({name: filter_name, filter_id: filter_id});
              }
            }else{
              this.labelFilterNames[x] = [{name: filter_name, filter_id: filter_id}];
            }
        });
        console.log(wanted_tsne_points);
        let next_chart_idx = this.options[0].series.findIndex(x => x.filter_key === "toberemove");
        //console.log(next_chart_idx);
        if(next_chart_idx !== -1){
          this.options[i].series[next_chart_idx].data = wanted_tsne_points;
          this.options[i].series[next_chart_idx].filter_key = filter_id;
          this.options[i].legend.data.push(filter_name);
          //console.log(this.option.legend);
        }else{
          this.options[i].series.push({name: filter_name, type: "scatter", data: wanted_tsne_points, filter_key: filter_id});
        }
        this.toggle.quickFilterMenu = false;
        this.quickFilter = [];
      }
    },
    removeFilter(index) {
      const key_to_remove = this.labelFilters[index].key;
      const chart_idx_to_remove = this.options[0].series.findIndex(x => x.filter_key === key_to_remove);
      for(let i=0; i<this.spaceTabs.length; i++){
        // remove filter legend
        this.options[i].legend.data = this.options[i].legend.data.filter(x => x != this.labelFilters[index].name);
        // remove filter result from chart
        this.options[i].series[chart_idx_to_remove].data = [];
        this.options[i].series[chart_idx_to_remove].filter_key = "toberemove";
      }
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
    performEntityFilter() {
      const that = this;
      const wanted_item = [];
      this.entityFilter.forEach(label_index =>{
        that.$store.state.df.items.filter(x => x.labels[label_index] === 1)
          .forEach(y => wanted_item.includes(y.index)? void(0):wanted_item.push(y.index));
      })
      if(this.$store.state.builtin.isBuiltIn){
        this.$store.dispatch('importDefaultTsne',{dataset: this.$store.state.builtin.dataset, entities: JSON.stringify(wanted_item)})
        .then(x => {
          if(x.success){
            this.labelFilters = [];
            this.labelFilterNames = [];
            for(let i=0; i<this.spaceTabs.length; i++){
              this.options[i].legend.data = [];
              let seriesLength = JSON.parse(JSON.stringify(this.options[i].series.length));
              for(let j=0; j<seriesLength; j++){
                this.options[i].series.pop();
              }
            }

            axios.get(this.$store.state.helper.apiAddr+"/builtin/tsne", {params: {dataset: this.$store.state.builtin.dataset,
            entities: JSON.stringify(wanted_item), type: "label"}})
            .then(res => res.data)
            .then(x => {
              this.options[0].series=[{ symbolSize: 10, data: x.tsne, type: "scatter" }]
            })

            axios.get(this.$store.state.helper.apiAddr+"/builtin/tsne", {params: {dataset: this.$store.state.builtin.dataset,
            entities: JSON.stringify(wanted_item), type: "feature"}})
            .then(res => res.data)
            .then(x => {
              this.options[1].series=[{ symbolSize: 10, data: x.tsne, type: "scatter" }]
            })

            this.toggle.entityFilterMenu = false;
          }
        })
        .catch(err => console.error(err));
      }
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
              for(let i=0; i<this.spaceTabs.length; i++){
                let seriesLength = JSON.parse(JSON.stringify(this.options[i].series.length));
                for(let j=1; j<seriesLength; j++){
                  this.options[i].series.pop();
                }
              }
              this.options[0].series[0].data=[];
              this.options[0].series[0].data = this.$store.state.tsne.label;
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
                  let new_point = this.$store.state.tsne.label[x];
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
                this.options[0].series.push({name: filter_name, type: "scatter", data: wanted_tsne_points, filter_key: filter_id});
                this.options[0].legend.data.push(filter_name);
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
    },
    spaceTabOnChange() {
      console.log("selcting: " + this.spaceTabs[this.spaceTab].tsne_type)
    },
    chartDebug() {
      console.log("options",this.options);
    },
    loadCluster() {
      let startTime = Date.now();
      if(this.$store.state.builtin.isBuiltIn){
        let requestUrl = `${this.$store.state.helper.apiAddr}/builtin/cluster?dataset=${this.$store.state.builtin.dataset}&nolabel=${this.$store.state.builtin.noLabel?1:0}`;
        axios.get(requestUrl)
        .then(res => res.data)
        .then(x => {
          const clusterResult = x.cluster_result;
          for(let [idx,item] of clusterResult.entries()){
            let filter_id = this.$store.state.helper.guid();
            let filter_name = "Cluster " + idx;
            let clusterCondition = [{field: "Cluster", operator: "Kmeans", value: item, key: this.$store.state.helper.guid()}];
            this.labelFilters.push({name: filter_name, conditions: clusterCondition, key: filter_id});
            for(let i=0; i<this.spaceTabs.length; i++) {
              let wanted_tsne_points = [];
              item.forEach( x => {
                let new_point = this.$store.state.tsne[this.spaceTabs[i].tsne_type][x];
                /*console.log(new_point)*/
                new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
                wanted_tsne_points.push(new_point);
                if(this.labelFilterNames[x]){
                  if(!this.labelFilterNames[x].map(y => y.name).includes(filter_name)){
                    this.labelFilterNames[x].push({name: filter_name, filter_id: filter_id});
                  }
                }else{
                  this.labelFilterNames[x] = [{name: filter_name, filter_id: filter_id}];
                }
              });
              this.options[i].series.push({name: filter_name, type: "scatter", data: wanted_tsne_points,
              filter_key: filter_id, df_indexs: JSON.parse(JSON.stringify(item))});
              this.options[i].legend.data.push(filter_name);
            }
          }
          let elaspedTime = Date.now() - startTime;
          this.toggle.clusterDialog = false;
          this.snackbar.success = true;
          this.snackbar.msg = "加载聚类结果成功 用时 "+ elaspedTime + " ms";
        })
        .catch(err => console.error(err))
      };
    }
  },
  computed: {
    getDatasetFields(){
      return this.$store.state.df.fields.map(x => x.name).filter(y => {
        const blackList = ["index","labels"];
        return !blackList.includes(y);
      })
    },
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
        const chart_idx_to_find = this.options[0].series.findIndex(x => x.filter_key === key_to_find);
        //console.log(this.options[0].color[chart_idx_to_find],key_to_find);
        return this.options[0].color[chart_idx_to_find];
      }
    },
    getTooltipBull(){
      return function(key){
        const chart_idx_to_find = this.options[0].series.findIndex(x => x.filter_key === key);
        return `<span style="color: ${this.options[0].color[chart_idx_to_find]}; font-size: 1rem">&bull;&nbsp;</span>`
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
        const current_filter = this.options[0].series.filter(x => x.filter_key === filter_key);
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
              //console.log(label_index);
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
      //console.log(z);
      return z;
    },
    filterOnClick(event,index) {
      console.log(event,index)
      //toggle.editorDialog[idx] = true;
    }
  }
}
</script>

<style scoped>
</style>