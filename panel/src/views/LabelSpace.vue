<template>
  <div>
    <v-container fluid>
      <v-row align="center" justify="space-between" style="height: 90vh">
        <v-col cols="12" md="8" class="fill-height d-flex flex-column">
          <v-card outlined class="mx-auto" style="height: 100%; width: 100%;">
            <v-card-text class="fill-height d-flex flex-column align-center justify-center rounded">
              <v-progress-circular v-if="!options[spaceTab].series[0].data.length" indeterminate></v-progress-circular>
              <v-chart v-show="options[spaceTab].series[0].data.length" style="height: 100%; width: 100%;" :option="options[spaceTab]" autoresize ref="mychart" />
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
                    <v-btn class="mr-2" text @click="chartDebug">Graph Filters</v-btn>
                  </span>
                  <span>
                  <v-menu bottom :close-on-click="true" :close-on-content-click="false" v-model="toggle.quickFilterMenu">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn dark color="indigo" class="mr-2" v-bind="attrs" v-on="on">
                        <v-icon>mdi-filter</v-icon>
                      </v-btn>
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
                        <v-btn color="primary" :disabled="!quickFilter.length" text @click="quickCreateFilter">Create</v-btn>
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
                  <v-row v-for="item in this.$store.state.graphFilter" :key="item.id" dense justify="space-between">
                    <v-col cols="10">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on" @click="filterOnClick(item)">
                            <div class="d-flex align-center" style="margin-left: -12px; width:100%; ">
                            <span :style="{'color': getFilterColor(item), 'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.name}} {{getFilterItemCount(item)}}</span>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="2">
                      <v-btn small text @click="removeFilter(item.id)"><v-icon>mdi-delete-forever</v-icon></v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-card-actions class="justify-center" style="position: absolute; left: 50%; top: 88%; transform: translate(-50%,-50%);">
              </v-card-actions>
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
    <v-card v-if="toggle.subChartDialog" style="position: absolute; top: 16%; left: 40px; width: 800px; height: 480px">
      <v-card-title>
        {{subChartDialog.currentTitle}}
        <v-btn icon style="position: absolute; left: 752px" @click="toggle.subChartDialog = false"><v-icon>mdi-close</v-icon></v-btn>
      </v-card-title>
      <v-card-text>
        <v-chart style="height: 400px; width: 100%;" :option="subChartDialog.options" autoresize/>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import { BrushComponent, ToolboxComponent, GridComponent, LegendComponent, TitleComponent, TooltipComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import axios from 'axios';

use([
  BarChart,
  CanvasRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  BrushComponent,
  ToolboxComponent
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
      if(!Object.keys(this.$store.state.graphFilter).length){ // length > 0 means graphFilters already exist
        this.toggle.clusterDialog = true;
      }
    }
    if(!this.$store.state.df.items.length){
      this.snackbar.msg = "无数据，即将跳转回主页";
      this.snackbar.success = true;
      setTimeout(() => {this.$router.push('/')}, 3000); // redirect after 3 sec if no data
    }
  },
  mounted() {
    for(let i=0; i<this.spaceTabs.length; i++){
      this.options[i].series[0].data = new Array();
      this.options[i].series[0].data = this.$store.state.tsne[this.spaceTabs[i].tsne_type];
    }
    this.newFilter = [{ field: "Labels", operator: "Contain", value: [], key: this.$store.state.helper.guid()}];
    if(Object.keys(this.$store.state.graphFilter).length){ // length > 0 means graphFilters already exist
      const graphFilter = this.$store.state.graphFilter;
      for(let filter_key in graphFilter){
        let filter_name = graphFilter[filter_key].name;
        let wanted_index = [];
        graphFilter[filter_key].conditions.forEach(cond => {
          cond.value.forEach(x => wanted_index.includes(x)? void(0):wanted_index.push(x));
        });
        for(let i=0; i<this.spaceTabs.length; i++) {
          let wanted_tsne_points = [];
          wanted_index.forEach( x => {
            let new_point = this.$store.state.tsne[this.spaceTabs[i].tsne_type][x];
            new_point[2] = {name: filter_name, df_index: x, filter_id: filter_key};
            wanted_tsne_points.push(new_point);
          });
          this.options[i].series.push({name: filter_name, type: "scatter", data: wanted_tsne_points,
          filter_key: filter_key, df_indexs: wanted_index});
          this.options[i].legend.data.push(filter_name);
        }
      }
    }
    this.$refs.mychart.chart.on("brushselected", (params) => {
      let selected = params.batch[0].selected[0].dataIndex;
      if(selected.length){
        alert(`选中${selected.length}个点：${selected}`);
        this.$refs.mychart.dispatchAction({type: "brush", areas: []});
      }
    })
  },
  data() {
    return {
      toggle: {
        filterDialog: false,
        editorDialog: false,
        quickFilterMenu: false,
        entityFilterMenu: false,
        clusterDialog: false,
        subChartDialog: false
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
      formData: {
        figureField: "",
        figureType: ""
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
        brush: {
          toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
          throttleType: "debounce",
          throttleDelay: 1000
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
              filter_of_data.forEach(x => tooltip_html += this.getTooltipBull(x.filter_id) + x.name + "</br>");
            }
            if(label_of_data.length){
              tooltip_html += "Labels (NUM): </br>".replace("NUM",label_of_data.length);
              for(let item of label_of_data){
                tooltip_html += this.getTooltipBull(-1) + item.name.replace("\\","") + "</br>";
              }
            }else{
              tooltip_html += "No Labels";
            };
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
      },
      subChartDialog: {
        currentFilterId: "",
        currentTitle: "",
        options: {
          xAxis: {
            type: 'category',
            data: [],
            nameLocation: 'center'
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: [],
            type: 'bar'
          }]
        }
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
    quickCreateFilter() {
      // push filter to labelFilters array
      let quickFilterQuery = new Array(this.$store.state.df.labels.length).fill(0);
      let filter_name = "";
      this.quickFilter.forEach(x => quickFilterQuery[x] = 1);
      if(this.quickFilter.length > 1){
        filter_name = `Contains \"${this.$store.state.df.labels[this.quickFilter[0]]}\" and ${this.quickFilter.length - 1} more`;
      }else{
        filter_name = `Contains \"${this.$store.state.df.labels[this.quickFilter[0]]}\"`;
      }
      axios.get(this.$store.state.helper.apiAddr+"/builtin/search/label",
      {params: {dataset: this.$store.state.builtin.dataset, query: JSON.stringify(quickFilterQuery)}})
      .then(res => res.data)
      .then(res_data => {
        let filter_id = this.$store.state.helper.guid();
        let filterCondition = [{field: "Labels", operator: "Contain", query: quickFilterQuery, value: res_data.query_result, key: this.$store.state.helper.guid()}];
        this.$store.dispatch('pushFilter',{id: filter_id, name: filter_name, conditions: filterCondition, field: "graphFilter"});
        let next_chart_idx = this.options[0].series.findIndex(x => x.filter_key === "toberemove");
        for(let i=0; i<this.spaceTabs.length; i++) {
          let wanted_tsne_points = [];
          res_data.query_result.forEach( y => {
            let new_point = this.$store.state.tsne[this.spaceTabs[i].tsne_type][y];
            new_point[2] = {name: filter_name, df_index: y, filter_id: filter_id};
            wanted_tsne_points.push(new_point);
          });
          if(next_chart_idx !== -1){
            this.options[i].series[next_chart_idx].name = filter_name;
            this.options[i].series[next_chart_idx].data = wanted_tsne_points;
            this.options[i].series[next_chart_idx].filter_key = filter_id;
            this.options[i].series[next_chart_idx].df_indexs = JSON.parse(JSON.stringify(res_data.query_result));
            this.options[i].legend.data[next_chart_idx] = filter_name;
          }else{
            this.options[i].series.push({name: filter_name, type: "scatter", data: wanted_tsne_points,
            filter_key: filter_id, df_indexs: JSON.parse(JSON.stringify(res_data.query_result))});
            this.options[i].legend.data.push(filter_name);
          }
        }
      })

      this.toggle.quickFilterMenu = false;
      this.quickFilter = [];
    },
    removeFilter(filter_key) {
      // remove filter plot
      const filter_name = this.$store.state.graphFilter[filter_key];
      const chart_idx_to_remove = this.options[0].series.findIndex(x => x.filter_key === filter_key);
      for(let i=0; i<this.spaceTabs.length; i++){
        // remove filter legend
        this.options[i].legend.data = this.options[i].legend.data.filter(x => x !== filter_name);
        // remove filter result from chart
        this.options[i].series[chart_idx_to_remove].data = [];
        this.options[i].series[chart_idx_to_remove].filter_key = "toberemove";
      }
      // remove filter
      this.$store.dispatch('deleteFilter', {id: filter_key, field: "graphFilter"});
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
      console.log(this.entityFilter);
    },
    spaceTabOnChange() {
      console.log("selcting: " + this.spaceTabs[this.spaceTab].tsne_type)
    },
    chartDebug() {
      console.log("options",this.options);
      console.log("subChartDialog",this.subChartDialog);
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
            this.$store.dispatch('pushFilter',{id: filter_id, name: filter_name, conditions: clusterCondition, field: "graphFilter"});
            for(let i=0; i<this.spaceTabs.length; i++) {
              let wanted_tsne_points = [];
              item.forEach( x => {
                let new_point = this.$store.state.tsne[this.spaceTabs[i].tsne_type][x];
                new_point[2] = {name: filter_name, df_index: x, filter_id: filter_id};
                wanted_tsne_points.push(new_point);
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
    },
    filterOnClick(event){
      this.subChartDialog.currentFilterId = event.id;
      this.subChartDialog.currentTitle = event.name;
      let wanted_item=[];
      for(let cond of event.conditions){
        cond.value.forEach(x => wanted_item.includes(x)? void(0):wanted_item.push(x))
      }
      axios.get(this.$store.state.helper.apiAddr+"/builtin/search",
      {params: {dataset: this.$store.state.builtin.dataset,
      entities: JSON.stringify(wanted_item), field: "location"}})
      .then(res => res.data)
      .then(x => {
        let xAxisData = Object.keys(x);
        let yAxisData = [];
        for(let val of xAxisData){
          yAxisData.push(x[val]);
        }
        this.subChartDialog.options.xAxis.data = xAxisData;
        this.subChartDialog.options.series[0].data = yAxisData;
        this.subChartDialog.options.xAxis.name = "location";
      })
      .then(this.toggle.subChartDialog = true)
    },
    getFilterColor(filter_obj){
      let color_index = this.options[0].series.findIndex(x => x.filter_key === filter_obj.id);
      return color_index? this.options[0].color[color_index]:this.options[0].color[0]
    },
    getFilterItemCount(filter_key){
      let current_filter = this.options[0].series.filter(x => x.filter_key === filter_key);
      if(current_filter.length){
        return "(" + current_filter[0].data.length + ")";
      }
    },
    getFilterNames(idx){ // find how many filters an index belongs to
      const graphFilter = this.$store.state.graphFilter;
      let matched = [];
      for(let filter_key in graphFilter){
        for(let cond of graphFilter[filter_key].conditions){
          if(cond.value.includes(idx)){
            matched.includes(graphFilter[filter_key].name)? void(0):matched.push({name: graphFilter[filter_key].name, filter_id: graphFilter[filter_key].id});
            break;
          }
        }
      }
      return matched;
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
    getTooltipBull(){
      return function(key){
        const chart_idx_to_find = this.options[0].series.findIndex(x => x.filter_key === key);
        return `<span style="color: ${this.options[0].color[chart_idx_to_find]}; font-size: 1rem">&bull;&nbsp;</span>`
      }
    }
  }
}
</script>

<style scoped>
</style>