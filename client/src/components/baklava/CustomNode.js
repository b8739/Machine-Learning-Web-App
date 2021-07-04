import { NodeBuilder } from "@baklavajs/core";

export default new NodeBuilder("CustomNodeWithBuilder", {
  twoColumn: true,
  width: 200
})
  .setName("Math")
  .addInputInterface("Input")
  .addOutputInterface("Output")
  .addOption("Open sidebar", "ButtonOption")
  .build();
