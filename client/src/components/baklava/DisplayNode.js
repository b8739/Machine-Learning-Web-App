import { NodeBuilder } from "@baklavajs/core";

export default new NodeBuilder("DisplayNode", {
  twoColumn: true,
  width: 200
})
  .setName("Debugger")
  .addInputInterface("In")

  .addOption("InputList", "TextOption")
  .addOption("Normalization", "TextOption")
  .addOption("AlgorithmName", "TextOption")
  .addOption("Parameters", "TextOption")
  .addOption("TargetList", "TextOption")

  .onCalculate(n => {
    let nodeResult = n.getInterface("In").value;
    if (nodeResult != null) {
      let inputList = "Inputs: " + JSON.stringify(nodeResult["inputs"]);
      let normalization = "Normalization: " + JSON.stringify(nodeResult["normalization"]);
      let algorithmName = "Algorithm Name: " + JSON.stringify(nodeResult["algorithm"]["name"]);
      let parameters = "Algorithm Name: " + JSON.stringify(nodeResult["algorithm"]["parameters"]);
      let targetList = "Targets: " + JSON.stringify(nodeResult["targets"]);
      n.setOptionValue("InputList", inputList);
      n.setOptionValue("Normalization", normalization);
      n.setOptionValue("AlgorithmName", algorithmName);
      n.setOptionValue("Parameters", parameters);
      n.setOptionValue("TargetList", targetList);
    }
    return nodeResult;
  })
  .build();
