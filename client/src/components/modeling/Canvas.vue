<template>
  <!-- konva 하던거 -->
  <!-- <div>
    <button @click="button">button</button>
    <v-stage ref="stage" :config="configKonva">
      <v-layer>
        <Block />
        <Block />
      </v-layer>
    </v-stage>
  </div> -->
  <div id="stage">
    <div id="myholder">hello</div>
  </div>
</template>
<script>
import Block from "@/components/modeling/Block.vue";

export default {
  methods: {},
  mounted() {
    //graph 정의
    let graph = new joint.dia.Graph();
    //paper 정의
    let paper = new joint.dia.Paper({
      el: $("#myholder"),
      width: 1000,
      height: 1000,
      model: graph,
      gridSize: 1
    });
    // line이 connect 되지 않으면 사라지도록
    paper.model.on("batch:stop", function() {
      var links = paper.model.getLinks();
      _.each(links, function(link) {
        var source = link.get("source");
        var target = link.get("target");
        if (source.id === undefined || target.id === undefined) {
          link.remove();
        }
      });
    });
    // default connector를 곡선으로 설정
    paper.options.defaultConnector = {
      name: "smooth",
      args: {
        radius: 20
      }
    };
    // Model 정의
    var shape = new joint.shapes.devs.Model({
      position: {
        x: 100,
        y: 100
      },
      inPorts: [""],
      outPorts: [" "]
    });
    // shape 화면의 render
    shape.addTo(graph);

    // let rect = new joint.shapes.standard.Rectangle({});

    // rect.position(100, 30);
    // rect.resize(100, 40);
    // rect.attr({
    //   body: {
    //     fill: "#a9a9a9",
    //     rx: 5,
    //     ry: 5
    //   },
    //   label: {
    //     text: "SVR",
    //     fill: "white"
    //   }
    // });

    // let rect2 = rect.clone();
    // rect2.translate(300);

    // var link = new joint.shapes.standard.Link();

    // link.source(rect);
    // link.target(rect2);

    // graph.addCells([rect, rect2, link]);

    // var link2 = new joint.shapes.standard.Link();
    // link2.prop("source", { x: 0, y: 0 });
    // link2.prop("target", { x: 200, y: 200 });
    // // link2.prop("vertices", [{ x: 450, y: 700 }]);
    // link2.attr("root/title", "joint.shapes.standard.Link");
    // link2.attr("line/stroke", "#fe854f");
    // link2.addTo(graph);
  }
};
</script>
<style>
#stage {
  width: 1000px;
  height: 1000px;
}
</style>
