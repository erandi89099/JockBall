package com.jockball;

import com.jockball.gear.SetBonus;
import com.jockball.item.ModItems;
import net.fabricmc.api.ModInitializer;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JockBall implements ModInitializer {
    public static final String MOD_ID = "jockball";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }

    @Override
    public void onInitialize() {
        ModItems.initialize();
        SetBonus.initialize();
        LOGGER.info("JockBall cargado: Fase 1 (armaduras, Trofeo y bonus de set).");
    }
}
