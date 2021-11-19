<template>
  <div>
    <v-container fluid>
      <v-row align="center" justify="space-between" style="height: calc(100vh - 60px)">
        <v-col cols="12" md="8" class="fill-height d-flex flex-column">
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
         <v-col class="fill-height d-flex flex-column"><v-row>
           <v-col cols="6" md="12">
             <v-card outlined class="px-4 pb-4 mx-auto fill-height">
               <v-card-title class="d-flex justify-space-between px-2">
                <span>分类器</span>
               </v-card-title>
               <v-card-text class="px-0 pb-0 mb-0 fill-height">
                 <v-row v-for="item in this.$store.state.graphFilter" :key="item.id" dense justify="space-between">
                    <v-col cols="10">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn color="warning" style="width: 100%" small block depressed outlined v-bind="attrs" v-on="on" @click="filterOnClick(item)">
                            <div class="d-flex align-center" style="margin-left: -12px; width:100%; ">
                            <span :style="{'color': item.color, 'margin-top': '-0.2rem', 'font-size': '2rem'}">&bull;</span>
                            <span style="text-align: left; width: 16rem; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.name }}</span>
                            </div>
                          </v-btn>
                        </template>
                          <span>{{item.name}}</span>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="2">
                      <v-btn small text @click="deleteGroup(item.id)"><v-icon>mdi-delete-forever</v-icon></v-btn>
                    </v-col>
                  </v-row>
               </v-card-text>
             </v-card>
           </v-col>
         </v-row></v-col>
      </v-row>
    </v-container>
    <v-dialog v-model="newGroupDialog.toggle" persistent max-width="400">
      <v-card class="pb-2">
        <v-card-title>
          建立新分类器
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
           <v-btn plain>No</v-btn>
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
    this.redrawGraph();
    this.setColorPalette();
    this.$refs.mychart.chart.on("brushselected", (params) => {
      let selected = params.batch[0].selected[0].dataIndex;
      selected = selected.map(x => this.option.series[0].data[x][2])
      if(selected.length){
        this.newGroupDialog.points = selected;
        this.newGroupDialog.toggle = true;
        this.$refs.mychart.dispatchAction({type: "brush", areas: []});
      }
    })
  },
  data() {
    return {
      colorPalette: {
        notUsed: ['#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0'],
        used: []
      },
      option: { // option 0 for label space
        xAxis: { type: "value" },
        yAxis: { type: "value" },
        dataZoom: { type: "inside"},
        tooltip: {
          trigger: "item",
          position: "top",
          formatter: (params) => {
            return params.data[2];
          }},
        brush: { 
          toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
          throttleType: "debounce",
          throttleDelay: 1000
        },
        series: [{
          filter_id: null,
          symbolSize: 10,
          type: "scatter",
          data: [],
          itemStyle: {
            borderColor: '#555',
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
      for(let filter of this.$store.state.graphFilter){
        let new_series_data = [];

        for(let point of filter.points){
          new_series_data.push([this.$store.state[current_tsne_table][point].x,this.$store.state[current_tsne_table][point].y,this.$store.state[current_tsne_table][point].id])
        }

        this.option.series.push({type: "scatter", data: new_series_data, filter_id: filter.id, 
        symbolSize: 10, itemStyle: { color: filter.color }});
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

      let new_series_data = [];

      for(let point of points){
        new_series_data.push([this.$store.state.tsne_label[point].x,this.$store.state.tsne_label[point].y,this.$store.state.tsne_label[point].id])
      }

      this.option.series.push({type: "scatter", data: new_series_data, filter_id: id, 
      symbolSize: 10, itemStyle: { color: color }});
    },
    deleteGroup(filter_id) {
      let targetIndex = this.option.series.findIndex(x => x.filter_id === filter_id);
      let targetColor = this.option.series[targetIndex].itemStyle.color;
      /*this.option.series = this.option.series.filter(x => x.filter_id !== filter_id)*/
      this.$store.dispatch("removeGraphFilter",{table:"graphFilter", id: filter_id});
      this.colorPalette.notUsed.push(targetColor);
      this.$forceUpdate();
      this.redrawGraph();
    }
  },
  computed: {
  }
}
</script>

<style scoped>
</style>