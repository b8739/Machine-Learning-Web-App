import { NodeBuilder } from "@baklavajs/core";

export default new NodeBuilder("DisplayNode", {
  twoColumn: true,
  width: 200
})
  .setName("Display")
  .addInputInterface("In")

  .addOption("InputList", "TextOption")
  .addOption("AlgorithmName", "TextOption")
  .addOption("Parameters", "TextOption")
  .addOption("TargetList", "TextOption")

  .onCalculate(n => {
    let nodeResult = n.getInterface("In").value;
    if (nodeResult != null) {
      let inputList = "Inputs: " + JSON.stringify(nodeResult["inputs"]);
      let algorithmName = "Algorithm Name: " + JSON.stringify(nodeResult["algorithm"]["name"]);
      let parameters = "Algorithm Name: " + JSON.stringify(nodeResult["algorithm"]["parameters"]);
      let targetList = "Targets: " + JSON.stringify(nodeResult["targets"]);
      n.setOptionValue("InputList", inputList);
      n.setOptionValue("AlgorithmName", algorithmName);
      n.setOptionValue("Parameters", parameters);
      n.setOptionValue("TargetList", targetList);
    }
    return nodeResult;
  })
  .build();
