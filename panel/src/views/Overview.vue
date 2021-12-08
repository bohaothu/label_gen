<template>
<div>
  <v-container fluid>
    <v-row dense>
      <v-col cols="4">
        <v-card class="fill-height">
          <v-card-text>
            <v-row align="start" justify="space-between" no-gutters class="fill-height" stlye="height: 680px;">
              <v-col cols="8">
                <v-row no-gutters style="margin-top: -4px; width: 150px;">
                  <v-col cols="12" class="text-h6 mb-1">{{this.$store.state.dataset}}</v-col>
                  <v-col cols="8">Features</v-col><v-col cols="4">{{this.$store.state.overview.attribute.length}}</v-col>
                  <v-col cols="8">Labels</v-col><v-col cols="4">{{this.$store.state.overview.labels.length}}</v-col>
                </v-row>
              </v-col>
              <v-col cols="4" >
                <v-row class="text-h1 pt-3" style="margin-left: -40px">{{Object.keys(this.$store.state.feature).length}}</v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="fill-height">
          <v-card-text>
            <v-row align="start" justify="space-between" no-gutters stlye="height: 720px">
              <v-col cols="8">
                <v-row no-gutters style="margin-top: -4px; width: 150px">
                  <v-col cols="12" class="text-h6 mb-1">Features</v-col>
                  <v-col cols="8">Instances</v-col><v-col cols="4">{{this.$store.state.overview.attribute.length}}</v-col>
                  <v-col cols="8">Numeric</v-col><v-col cols="4">{{this.$store.state.overview.attribute.filter(x => x.type === "numeric").length}}</v-col>
                  <v-col cols="8">Nominal</v-col><v-col cols="4">{{this.$store.state.overview.attribute.filter(x => x.type === "nominal").length}}</v-col>
                </v-row>
              </v-col>
              <v-col cols="4" >
                <v-chart style="height: 100%; width: 100%;" :option="attrOption" autoresize />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="fill-height">
          <v-card-text>
            <v-row align="start" justify="space-between" no-gutters class="fill-height" stlye="height: 680px;">
              <v-col cols="8">
                <v-row no-gutters style="margin-top: -4px; width: 150px;">
                  <v-col cols="12" class="text-h6 mb-1">Labels</v-col>
                  <v-col>{{truncatedLabels}}</v-col>
                </v-row>
              </v-col>
              <v-col cols="4" >
                <v-row class="text-h1 pt-3 ml-1">{{this.$store.state.overview.labels.length}}</v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      
    </v-row>
  </v-container>
</div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { LegendComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  PieChart,
  CanvasRenderer,
  LegendComponent
]);

export default {
  name: "Overview",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "light"
  },
  mounted() {
    if(!Object.keys(this.$store.state.tsne_feature).length){
      this.$store.dispatch('importTsne',{dataset: this.$store.state.dataset})
    }
  },
  data() {
    return {
      attrOption: {
        series: [{
          type: "pie",
          radius: '100%',
          data: [{name: "numeric", value: this.$store.state.overview.attribute.filter(x => x.type === "numeric").length},
          {name: "nominal", value: this.$store.state.overview.attribute.filter(x => x.type === "nominal").length}]
        }]
      }
    }
  },
  methods: {
    
  },
  computed: {
    truncatedLabels() {
      let truncatedText = "";
      for(let item of this.$store.state.overview.labels){
        if(truncatedText.length < 50){
          truncatedText += item + ", ";
        }else{
          truncatedText += " ...";
          break;
        }
      }
      return truncatedText;
    }
  }
}
</script>
