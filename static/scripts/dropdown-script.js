$(function () {
    $("#server-dropdown").on("change", function () {
        switch ($(this).val()) {
            case "":
                $("#server-text").html("");
                break;
            case "vanilla-mc-server":
            	$("#server-text").html(
            		function() {
            		    var name = "Vanilla Minecraft";
                        var minecraft_version = "1.15.2";
            		    var description = "Vanilla Minecraft survival.";
                        var requirements = "Vanilla Minecraft";
            			return "<strong>Name:</strong> " + name + "<br>" +
                            "<strong>Description:</strong> " + description + "<br>" +
                            "<strong>Requirements:</strong> Minecraft version " + minecraft_version + (requirements ? (", " + requirements + "<br>") : "");
            		}
            		);
                break;
            case "ricebuild-mc-server":
            	$("#server-text").html(
            		function() {
            		    var name = "Rice University Build";
                        var minecraft_version = "";
            		    var description = "Rice University built in Minecraft.";
                        var requirements = "";
            			return "<strong>Name:</strong> " + name + "<br>" +
                            "<strong>Description:</strong> " + description + "<br>" +
                            "<strong>Requirements:</strong> Minecraft version " + minecraft_version + (requirements ? (", " + requirements + "<br>") : "");
            		}
            		);
                break;
        }
    });
});