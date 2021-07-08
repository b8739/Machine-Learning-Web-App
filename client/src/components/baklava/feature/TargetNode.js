import { NodeBuilder } from "@baklavajs/core";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import store from "@/store/index";

const columns = store.getters["initialData/columns"];

export default new NodeBuilder("TargetNode", {})
  .setName("Target")
  .addInputInterface("IN")
  .addOutputInterface("OUT")
  // .addOption("FeatureOption", "FeatureOption")
  .addOption(
    "Features",
    "ButtonOption",
    () => {
      return { features: columns };
    },
    "FeatureSidebar"
  )

  // .addOption("ValueText", "TextOption")
  .onCalculate(n => {
    let nodeResult = n.getInterface("IN").value;
    let targets = n.getOptionValue("Features");
    if (nodeResult != null) {
      nodeResult["targets"] = targets;
      n.getInterface("OUT").value = nodeResult;
      return nodeResult;
    }
    console.log("ca");

    // n.setOptionValue("ValueText", result);
  })
  .build();
