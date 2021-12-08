<template>
  <div>
    <v-container fluid class="pa-1">
      <v-row align="stretch" justify="space-between" style="height: calc(100vh - 16px)" dense>
        <v-col cols="9" class="fill-height d-flex flex-column">
          <v-card outlined class="mx-auto" style="height: 100%; width: 100%;">
            <v-card-text class="fill-height d-flex flex-column align-center justify-center rounded">
              <v-chart style="height: 100%; width: 100%;" :option="option" autoresize ref="mychart" />
              <v-btn-toggle v-model="spaceTab" @change="spaceTabOnChange">
                <v-btn v-for="item in spaceTabs" :key="item.tab">
                  <v-icon small left>{{ item.icon }}</v-icon> {{ item.tab }}
                </v-btn>
              </v-btn-toggle>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="3" class="d-flex flex-column">
          <v-card outlined class="fill-height px-4 pb-4 mx-auto mb-2 flex-grow-1" style="width: 100%">
               <v-card-title class="d-flex justify-space-between px-2">
                <span>分组</span>
                <span>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn icon color="primary" v-bind="attrs" v-on="on"><v-icon>mdi-plus</v-icon></v-btn>
                    </template>
                    <span>新建分组</span>
                  </v-tooltip>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn icon color="secondary" v-bind="attrs" v-on="on" @click="saveFilter"><v-icon>mdi-content-save</v-icon></v-btn>
                    </template>
                    <span>保存分组</span>
                  </v-tooltip>
                </span>
               </v-card-title>
               <v-card-text class="px-0 pb-0 mb-0 fill-height">
                 <v-row v-for="item in this.$store.state.graphFilter" :key="item.id" dense justify="space-between">
                    <v-col cols="11">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on" @click="filterOnClick(item)">
                            <div class="d-flex align-center ml-4" style="width:100%;">
                            <span :style="{'color': item.color, 'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.name}}</span>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="1">
                      <v-btn small icon @click="deleteGroup(item.id)"><v-icon>mdi-delete-forever</v-icon></v-btn>
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
  </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import { BrushComponent, ToolboxComponent, DataZoomComponent, GridComponent, LegendComponent, TitleComponent, TooltipComponent } from "echarts/components";
import VChart, { THEME_KEY, UPDATE_OPTIONS_KEY } from "vue-echarts";
import { saveAs } from "file-saver";

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
    if(!Object.keys(this.$store.state.tsne_feature).length){
      this.$store.dispatch('importTsne',{dataset: this.$store.state.dataset})
    }
    this.redrawGraph();
    this.setColorPalette();
    if(Object.keys(this.$store.state.feature).length){
      this.redrawGraph();
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
    }
  },
  data() {
    return {
      colorPalette: {
        notUsed: ['#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0'],
        used: []
      },
      displayPreference: {
        notShowZeroLabelPoint: false,
        symbolSizeByLabelCount: false
      },
      echartEvents: {
        legendselected: {}
      },
      option: { // option 0 for label space
        xAxis: { type: "value" },
        yAxis: { type: "value" },
        legend: { y: "top", data: ["No Group"] },
        dataZoom: { type: "inside"},
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
        series: [{
          name: "No Group",
          filter_id: null,
          symbolSize: this.getSymbolSize,
          type: "scatter",
          data: [],
          itemStyle: {
            opacity: 0.5,
            color: "#bbb"
        }}]
      },
      newGroupDialog: {
        toggle: false,
        name: "",
        points: []
      },
      currentPoint: -1,
      spaceTab: 0,
      spaceTabs: [
        { tab: "Label Space", icon: "mdi-tag", tsne_type: "label", tsne_table: "tsne_label"},
        { tab: "Feature Space", icon: "mdi-pound", tsne_type: "feature", tsne_table: "tsne_feature"}
      ],
      quickFilter: [],
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
    setColorPalette() {
      let usedColor = this.$store.state.graphFilter.map(x => x.color);
      this.colorPalette.used = usedColor;
      this.colorPalette.notUsed = this.colorPalette.notUsed.filter(x => !usedColor.includes(x));
    },
    redrawGraph() {
      let current_tsne_table = this.spaceTabs[this.spaceTab].tsne_table;
      this.option.series.splice(1); // only keep the first series
      this.option.series[0].data = Object.values(this.$store.state[current_tsne_table]).map(z => [z.x,z.y,z.id]);
      this.option.series[0].data = this.option.series[0].data.filter(x => this.labelCountFilterResult.includes(x[2]));
      for(let filter of this.$store.state.graphFilter){
        let new_series_data = [];

        for(let point of filter.points){
          if(this.labelCountFilterResult.includes(point)){
            new_series_data.push([this.$store.state[current_tsne_table][point].x,this.$store.state[current_tsne_table][point].y,this.$store.state[current_tsne_table][point].id]);
            this.option.series[0].data = this.option.series[0].data.filter(x => x[2] !== point);
          }        
        }

        this.option.series.push({type: "scatter", data: new_series_data, filter_id: filter.id, 
        symbolSize: this.getSymbolSize, itemStyle: { color: filter.color }, name: filter.name});
        this.option.legend.data.push(filter.name);
      }
      if(Object.keys(this.echartEvents.legendselected).length){
        this.option.legend.selected = this.echartEvents.legendselected;
      }
    },
    spaceTabOnChange() {
      this.redrawGraph();
    },
    submitNewGroup() {
      let points = this.newGroupDialog.points;
      let color = this.colorPalette.notUsed.shift();
      let id = this.$store.state.helper.guid();
      this.colorPalette.used.push(color);
      this.$store.dispatch("addGraphFilter",{value: {name: this.newGroupDialog.name, 
      points: points, color: color, id: id}})
      this.newGroupDialog.toggle = false;

      this.redrawGraph();
    },
    deleteGroup(filter_id) {
      let targetIndex = this.option.series.findIndex(x => x.filter_id === filter_id);
      let targetColor = this.option.series[targetIndex].itemStyle.color;
      this.$store.dispatch("removeGraphFilter",{table:"graphFilter", id: filter_id});
      this.colorPalette.notUsed.push(targetColor);
      this.redrawGraph();
    },
    labelCountFilter(min, max){
      let z=[];
      for(let item in this.labelCount){
        if(this.labelCount[item] >= min && this.labelCount[item] <= max){
          z.push(item);
        }
      }
      return z;
    },
    notShowZeroLabelPointOnChange() {
      this.redrawGraph();
    },
    symbolSizeByLabelCountOnChange() {
      this.redrawGraph();
    },
    getSymbolSize(val, params) {
      return this.displayPreference.symbolSizeByLabelCount? 10 + 2 * this.labelCount[val[2]]:10;
    },
    saveFilter() {
      let outputContent = {dataset_name: this.$store.state.dataset, filters: this.$store.state.graphFilter}
      let outputBlob = new Blob([JSON.stringify(outputContent)], {type: "text/plain; charset=utf-8"});
      saveAs(outputBlob,"output.json");
    }
  },
  computed: {
    labelCount() {
      let z={};
      for(let item in this.$store.state.label){
        z[item] = Object.values( (({ id, ...o }) => o)(this.$store.state.label[item]) ).reduce((a, b) => a+b);
      }
      return z;
    },
    labelCountRange() {
      let arr = Object.values(this.labelCount);
      let min = Math.min(...arr);
      let max = Math.max(...arr);
      return [min, max];
    },
    labelCountFilterResult() {
      let min = this.displayPreference.notShowZeroLabelPoint? 1:0;
      let max = this.labelCountRange[1];
      return this.labelCountFilter(min,max);
    }
  }
}
</script>

<style scoped>
</style>