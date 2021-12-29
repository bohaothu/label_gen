<template>
  <div>
    <v-container fluid class="pa-1">
      <v-row align="stretch" justify="space-between" style="height: calc(100vh - 16px)" dense>
        <v-col cols="9" class="fill-height d-flex flex-column">
          <v-card outlined class="mx-auto" style="height: 100%; width: 100%;">
            <v-card-text class="d-flex flex-column align-center justify-center rounded pb-0" style="height: calc(100% - 72px)">
              <v-chart style="height: 100%; width: 100%;" :option="option" autoresize ref="mychart" />              
            </v-card-text>
            <v-card-actions>
            <v-row align="center" justify="space-between" style="margin-top: -20px">
              <v-col cols="4" class="d-flex justify-center">
                <v-radio-group v-model="dataSplit" row>
                  <v-radio v-for="item in dataSplits" :key="item" :label="`${item}`" :value="item"></v-radio>
                </v-radio-group>
              </v-col>
              <v-col cols="4">
              <v-btn-toggle v-model="spaceTab" @change="spaceTabOnChange">
                <v-btn v-for="item in spaceTabs" :key="item.tab">
                  <v-icon small left>{{ item.icon }}</v-icon> {{ item.tab }}
                </v-btn>
              </v-btn-toggle>
              </v-col>
              <v-col cols="4">
                </v-col>
            </v-row>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="3" class="d-flex flex-column">
          <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
               <v-card-title class="d-flex justify-space-between px-2">
                <span>分组</span>
                <span>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn icon color="primary" v-bind="attrs" v-on="on" @click="newQueryGroupDialog.toggle = true"><v-icon>mdi-plus</v-icon></v-btn>
                    </template>
                    <span>新建分组</span>
                  </v-tooltip>
                </span>
               </v-card-title>
               <v-card-text class="px-0 pb-0 mb-0 fill-height">
                 <v-row v-for="item in graphFilters" :key="item._id.$oid" dense justify="space-between">
                    <v-col cols="11">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on" @click="filterOnClick(item._id.$oid)">
                            <div class="d-flex align-center ml-4" style="width:100%;">
                            <span class="pl-1" :style="{'color': option.color[option.series.findIndex( x => x.name == item.group_name) - 1], 'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.group_name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.points.length}}</span>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="1">
                      <v-btn small icon @click="deleteGroup(item._id.$oid)"><v-icon>mdi-delete-forever</v-icon></v-btn>
                    </v-col>
                  </v-row>
               </v-card-text>
          </v-card>
          <v-card outlined class="px-4 pb-4 mx-auto flex-grow-1">
               <v-card-title class="d-flex justify-space-between px-2">
                <span>展示选项</span>
               </v-card-title>
               <v-card-text class="px-0 pb-0 mb-0">
                 <v-row align="center" justify="start" no-gutters>
                  <v-col cols="12">
                    <v-checkbox v-model="displayPreference.notShowZeroLabelPoint" label="隐藏无 Label 数据点" @change="notShowZeroLabelPointOnChange"></v-checkbox>
                  </v-col>
                  <v-col cols="12">
                     <v-checkbox v-model="displayPreference.symbolSizeByLabelCount" label="按 Label 数量改变数据点尺寸" @change="symbolSizeByLabelCountOnChange"></v-checkbox>
                   </v-col>
                 </v-row>
               </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog v-model="newGroupDialog.toggle" persistent max-width="400">
      <v-card class="pb-2">
        <v-card-title>
          建立新分组
        </v-card-title>
        <v-card-text>
          <v-row align="baseline" no-gutters>
            <v-col cols="4" class="text-body-1">名称</v-col>
            <v-col cols="8"><v-text-field v-model="newGroupDialog.name" dense outlined></v-text-field></v-col>
            <v-col cols="4" class="text-body-1">数量</v-col>
            <v-col cols="8">{{newGroupDialog.points.length}}</v-col>
          </v-row>
        </v-card-text>
         <v-card-actions class="justify-end pt-0">
           <v-btn color="primary" @click="submitNewGroup">Yes</v-btn>
           <v-btn plain @click="newGroupDialog.toggle = false">No</v-btn>
         </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="newQueryGroupDialog.toggle" persistent max-width="480">
      <v-card class="pb-2">
        <v-card-title>
          建立新分组
        </v-card-title>
        <v-card-text class="py-0">
          <v-row align="baseline" no-gutters class="mt-1">
            <v-col cols="12">
              <v-text-field v-model="newQueryGroupDialog.name"
              label="名称" dense outlined></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-autocomplete v-model="newQueryGroupDialog.wanted" :items="labelNames"
              label="包含这些标签" dense small-chips multiple outlined></v-autocomplete>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="justify-end pt-0">
           <v-btn color="primary" @click="submitNewQueryGroup">Yes</v-btn>
           <v-btn plain @click="newQueryGroupDialog.toggle = false">No</v-btn>
         </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="subChartDialog.toggle" max-width="640">
      <v-card>
        <v-card-title>
          <v-row align="stretch" justify="space-between">
            <v-col>
              这是标题
            </v-col>
            <v-col cols="1">
              <v-btn @click="subChartDialog.toggle = false" icon><v-icon>mdi-close</v-icon></v-btn>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text>
          包含的点数、包含的标签种类、包含的标签个数、训练 Binary Classifier、计算 Mutual Information <br>
          {{ subChartDialog.filterId }}
        </v-card-text>
        <v-card-actions>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import { BrushComponent, ToolboxComponent, DataZoomComponent, GridComponent, LegendComponent, TitleComponent, TooltipComponent } from "echarts/components";
import VChart, { THEME_KEY, UPDATE_OPTIONS_KEY } from "vue-echarts";
import axios from 'axios';

use([
  BarChart,
  CanvasRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  BrushComponent,
  ToolboxComponent,
  DataZoomComponent
]);

export default {
  name: 'LabelSpace',
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "light",
    [UPDATE_OPTIONS_KEY]: true
  },
  created() {
  },
  mounted() {
    this.fetchData();
    this.$refs.mychart.chart.on("brushselected", (params) => {
      let selected = params.batch[0].selected[0].dataIndex;
      selected = selected.map(x => this.option.series[0].data[x][2])
      if(selected.length){
        
        this.newGroupDialog.points = selected;
        this.newGroupDialog.toggle = true;
        this.$refs.mychart.dispatchAction({type: "brush", areas: []});
      }else{
        this.$refs.mychart.dispatchAction({type: "brush", areas: []});
      }
    })
    this.$refs.mychart.chart.on("legendselectchanged", (params) => {
      this.echartEvents.legendselected = params.selected;
    })
    
    /*
    if(Object.keys(this.$store.state.feature).length){
      this.redrawGraph();
      
      this.$refs.mychart.chart.on("legendselectchanged", (params) => {
        this.echartEvents.legendselected = params.selected;
      })
    }
    */
  },
  data() {
    return {
      dataSplit: "train",
      dataSplits: ["train", "test"],
      graphFilters: [],
      displayPreference: {
        notShowZeroLabelPoint: false,
        symbolSizeByLabelCount: false
      },
      echartEvents: {
        legendselected: {}
      },
      labelNames: [],
      option: { // option 0 for label space
        xAxis: { type: "value" },
        yAxis: { type: "value" },
        legend: { y: "top", data: [] },
        dataZoom: { type: "inside"},
        color: ['#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0'],
        tooltip: {
          trigger: "item",
          position: "top",
          formatter: (params) => {
            return params.data[2];
          }},
        brush: { 
          toolbox: ['rect', 'polygon', 'keep', 'clear'],
          throttleType: "debounce",
          throttleDelay: 1000
        },
        series: []
      },
      newGroupDialog: {
        toggle: false,
        name: "",
        points: []
      },
      newQueryGroupDialog: {
        toggle: false,
        name: "",
        wanted: []
      },
      currentPoint: -1,
      spaceTab: 0,
      spaceTabs: [
        { tab: "Feature Space", icon: "mdi-pound", tsne_type: "features"},
        { tab: "Label Space", icon: "mdi-tag", tsne_type: "labels"},
        { tab: "Label Combinations", icon: "mdi-format-list-group", tsne_type: "labels_combination"}
      ],
      quickFilter: [],
      snackbar: {
        success: false,
        msg: ""
      },
      subChartDialog: {
        toggle: false,
        filterId: ""
      }
    }
  },
  methods: {
    fetchData(){
      axios({
        method: "get",
        url: `/available/labels/${this.$store.state.dataset}`,
        baseURL: this.$store.state.helper.apiAddr
      }).then(res => res.data)
      .then(x => {
        this.labelNames = x.labels;
      })
      this.redrawGraph();
    },
    loadGroupFilters(){
      return axios({
        method: "get",
        url: `/group/load/${this.$store.state.dataset}/train`,
        baseURL: this.$store.state.helper.apiAddr
      })
    },
    importTsneWithQuery(tsne_type, params){
      return axios.get(`${this.$store.state.helper.apiAddr}/tsne/${tsne_type}/${this.$store.state.dataset}/train`,
      { params: params })
    },
    redrawGraph() {
      this.option.series = [];
      let current_tsne_type = this.spaceTabs[this.spaceTab].tsne_type;
      this.importTsneWithQuery(current_tsne_type, 
        { nolabel: this.displayPreference.notShowZeroLabelPoint? 1:0 })
      .then( res => res.data ) 
      .then( x => {
        this.option.series.push({
          name: "No Group",
          filter_id: null,
          symbolSize: this.getSymbolSize,
          type: "scatter",
          data: x.result,
          itemStyle: {
            opacity: 0.5,
            color: "#bbb"
        }})

        if(x.result.length){
          this.option.legend.data.push("No Group");
        }
      });
      
      this.loadGroupFilters()
      .then(res => res.data )
      .then( group => {
        this.graphFilters = group.groups;
        for(let item of this.graphFilters){
          this.importTsneWithQuery(current_tsne_type, {
            nolabel: this.displayPreference.notShowZeroLabelPoint? 1:0,
            filter_id: item._id.$oid})
          .then( res => res.data )
          .then(x => {
            this.option.series.push({type: "scatter", data: x.result, filter_id: x.filter_id, symbolSize: 10, name: item.group_name})
            this.option.legend.data.push(item.group_name);
          })
        }
      })
    },
    spaceTabOnChange() {
      this.redrawGraph();
    },
    submitNewGroup() {
      if(this.spaceTabs[this.spaceTab].tsne_type === "labels_combination"){
        axios({
          method: "post",
          url: `/group/add`,
          baseURL: this.$store.state.helper.apiAddr,
          headers: {"Content-Type": "application/json;charset=UTF-8"},
          data: { dataset_name: this.$store.state.dataset, dataset_type: "train",
          group_name: this.newGroupDialog.name, group_type: "selected_combination", 
          points: this.newGroupDialog.points.map(x => x.$oid)}
        }).then(() => {
          this.newGroupDialog.name = "";
          this.newGroupDialog.points = [];
          this.newGroupDialog.toggle = false;
          this.redrawGraph();
        })
      }else{
        axios({
          method: "post",
          url: `/group/add`,
          baseURL: this.$store.state.helper.apiAddr,
          headers: {"Content-Type": "application/json;charset=UTF-8"},
          data: { dataset_name: this.$store.state.dataset, dataset_type: "train",
          group_name: this.newGroupDialog.name, group_type: "selected", points: this.newGroupDialog.points}
        }).then(() => {
          this.newGroupDialog.name = "";
          this.newGroupDialog.points = [];
          this.newGroupDialog.toggle = false;
          this.redrawGraph();
        })  
      }
    },
    submitNewQueryGroup() {
      let query = {$or: []};
      this.newQueryGroupDialog.wanted.forEach(x => {
        let item  = {};
        item[x] = 1;
        query.$or.push(item);
      });

      axios({
        method: "post",
        url: `/group/add`,
        baseURL: this.$store.state.helper.apiAddr,
        headers: {"Content-Type": "application/json;charset=UTF-8"},
        data: { dataset_name: this.$store.state.dataset, dataset_type: "train",
        group_name: this.newQueryGroupDialog.name, group_type: "query", query: query}
      }).then(() => {
        this.newQueryGroupDialog.name = "";
        this.newQueryGroupDialog.wanted = [];
        this.newQueryGroupDialog.toggle = false;
        this.redrawGraph();
      })
    },
    deleteGroup(group_id) {
      this.graphFilters = this.graphFilters.find(item => item._id.$oid !== group_id);
      axios({
        method: "post",
        url: `/group/remove`,
        baseURL: this.$store.state.helper.apiAddr,
        headers: {"Content-Type": "application/json;charset=UTF-8"},
        data: { dataset_name: this.$store.state.dataset, dataset_type: "train", group_id: group_id}
      }).then(() => {
        this.redrawGraph();
      });
    },
    filterOnClick(item_id) {
      this.subChartDialog.toggle = true;
      this.subChartDialog.filterId = item_id;
    },
    notShowZeroLabelPointOnChange() {
      this.redrawGraph();
    },
    symbolSizeByLabelCountOnChange() {
      this.redrawGraph();
    },
    getSymbolSize(val, params) {
      return this.displayPreference.symbolSizeByLabelCount? 10 + 2 * this.labelCount[val[2]]:10;
    }
  },
  computed: {
  }
}
</script>

<style scoped>
</style>