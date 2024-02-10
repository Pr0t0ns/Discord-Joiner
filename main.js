import {world,system} from '@minecraft/server'

if(!world.scoreboard.getObjective("c")){
  world.scoreboard.addObjective("c", "Cps")
}

system.runInterval(()=>{
  world.getDimension("overworld").runCommand("scoreboard players add @a c 0")
})

world.afterEvents.playerInteractWithBlock.subscribe(ev => {
  const block = ev.block
  const player = ev.player
  
  if(block.typeId == "minecraft:diamond_block"){
    world.scoreboard.getObjective("c").addScore(player, 1)
    player.playSound("note.harp")
  }
})

system.runInterval(()=>{
  for(let player of world.getAllPlayers()){
    let hcps = player.getDynamicProperty("hcps") == null ? 0 : player.getDynamicProperty("hcps")
    let c = world.scoreboard.getObjective("c").getScore(player)
    let cObj = world.scoreboard.getObjective("c")
    
    if(hcps < c){
      player.sendMessage("§l§eNEW HIGHEST CPS: "+c)
      player.setDynamicProperty("hcps", c)
      cObj.setScore(player, 0)
      player.playSound("random.orb")
    }else{
      if(!c == 0){
        player.sendMessage("§aCps: "+c)
        cObj.setScore(player, 0)
      }
    }
  }
},20)