package com.jockball.item;

import com.jockball.JockBall;
import com.jockball.gear.GearLevel;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public final class ModItems {
    /** Nombres de las 4 piezas, en el orden de ArmorType: casco, pecho, fundas, botas. */
    public static final String[] PIECE_NAMES = {"helmet", "shoulder_pads", "pants", "cleats"};
    private static final ArmorType[] PIECE_TYPES =
            {ArmorType.HELMET, ArmorType.CHESTPLATE, ArmorType.LEGGINGS, ArmorType.BOOTS};

    /** GEAR[nivel-1][pieza] */
    public static final Item[][] GEAR = new Item[GearLevel.MAX][4];
    /** Nivel (1-5) de cada pieza de JockBall. */
    public static final Map<Item, Integer> LEVEL_OF = new HashMap<>();

    public static final Item TROPHY = register("trophy", Item::new, new Item.Properties());
    /** Plantilla de herreria: se consume en cada mejora, igual que la de netherite. */
    public static final Item UPGRADE_TEMPLATE = register("upgrade_template", Item::new, new Item.Properties());

    static {
        for (int level = 1; level <= GearLevel.MAX; level++) {
            ArmorMaterial material = GearLevel.material(level);
            for (int p = 0; p < 4; p++) {
                Item item = register(
                        PIECE_NAMES[p] + "_l" + level,
                        Item::new,
                        new Item.Properties()
                                .humanoidArmor(material, PIECE_TYPES[p])
                                .durability(PIECE_TYPES[p].getDurability(GearLevel.baseDurability(level))));
                GEAR[level - 1][p] = item;
                LEVEL_OF.put(item, level);
            }
        }
    }

    private static Item register(String name, Function<Item.Properties, Item> factory, Item.Properties props) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, JockBall.id(name));
        Item item = factory.apply(props.setId(key));
        return Registry.register(BuiltInRegistries.ITEM, key, item);
    }

    /** Nivel de una pieza, o 0 si no es equipamiento de JockBall. */
    public static int levelOf(net.minecraft.world.item.ItemStack stack) {
        return LEVEL_OF.getOrDefault(stack.getItem(), 0);
    }

    public static void initialize() {
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT).register(tab -> {
            for (Item[] row : GEAR) {
                for (Item item : row) {
                    tab.accept(item);
                }
            }
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(tab -> {
            tab.accept(TROPHY);
            tab.accept(UPGRADE_TEMPLATE);
        });
    }

    private ModItems() {}
}
