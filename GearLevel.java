package com.jockball.gear;

import com.jockball.JockBall;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;

import java.util.Map;

/**
 * Los 5 niveles de equipamiento. TODO el balance esta en esta tabla y en SetBonus:
 * si quieres cambiar numeros, es aqui.
 */
public final class GearLevel {
    public static final int MAX = 5;

    public static final TagKey<Item> REPAIRS_GEAR =
            TagKey.create(Registries.ITEM, JockBall.id("repairs_gear"));

    // Durabilidad base por nivel (como "multiplicador" vanilla: cuero 5, hierro 15, diamante 33, netherite 37)
    private static final int[] DURABILITY = {8, 14, 20, 30, 40};
    // Defensa propia de cada pieza: {casco, pecho, fundas, tachos}. El grueso va en el bonus de set.
    private static final int[][] DEFENSE = {{1, 2, 1, 1}, {1, 3, 2, 1}, {2, 4, 3, 1}, {2, 5, 4, 2}, {3, 6, 5, 2}};
    private static final float[] TOUGHNESS = {0f, 0f, 0f, 1f, 2f};
    private static final int[] ENCHANT = {8, 9, 10, 12, 15};

    private static Holder<SoundEvent> sound(int level) {
        return switch (level) {
            case 1 -> SoundEvents.ARMOR_EQUIP_LEATHER;
            case 2 -> SoundEvents.ARMOR_EQUIP_CHAIN;
            case 3 -> SoundEvents.ARMOR_EQUIP_IRON;
            case 4 -> SoundEvents.ARMOR_EQUIP_DIAMOND;
            default -> SoundEvents.ARMOR_EQUIP_NETHERITE;
        };
    }

    public static int baseDurability(int level) {
        return DURABILITY[level - 1];
    }

    public static ArmorMaterial material(int level) {
        int[] d = DEFENSE[level - 1];
        ResourceKey<EquipmentAsset> assetKey =
                ResourceKey.create(EquipmentAssets.ROOT_ID, JockBall.id("level_" + level));
        return new ArmorMaterial(
                baseDurability(level),
                Map.of(
                        ArmorType.HELMET, d[0],
                        ArmorType.CHESTPLATE, d[1],
                        ArmorType.LEGGINGS, d[2],
                        ArmorType.BOOTS, d[3]),
                ENCHANT[level - 1],
                sound(level),
                TOUGHNESS[level - 1],
                0.0F,
                REPAIRS_GEAR,
                assetKey);
    }

    private GearLevel() {}
}
