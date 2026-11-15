package com.jockball.gear;

import com.jockball.JockBall;
import com.jockball.item.ModItems;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.Holder;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;

/**
 * Bonus por set. El nivel efectivo es el de la pieza MAS BAJA; si falta una pieza, es 0.
 * (Con 3 piezas nivel 4 y una nivel 3 -> bonus de nivel 3.)
 *
 * Casco = Fuerza | Hombreras = Resistencia | Tachos = Velocidad | Fundas = Saturacion
 */
public final class SetBonus {
    // Indice 0 = nivel 1 ... indice 4 = nivel 5.  AJUSTA AQUI EL BALANCE.
    private static final double[] STRENGTH = {1.0, 2.0, 3.0, 4.5, 6.0};          // dano de ataque extra
    private static final double[] RESIST_ARMOR = {1.0, 2.0, 3.0, 4.0, 5.0};       // puntos de armadura extra
    private static final double[] RESIST_KB = {0.0, 0.0, 0.1, 0.2, 0.3};          // resistencia a empuje
    private static final double[] SPEED = {0.03, 0.06, 0.10, 0.15, 0.20};         // +% velocidad (0.20 = +20%)
    private static final float[] SATURATION = {0.5f, 1.0f, 1.5f, 2.0f, 3.0f};     // saturacion repuesta cada 2 s

    private static final Identifier ID_STR = JockBall.id("set_strength");
    private static final Identifier ID_ARM = JockBall.id("set_armor");
    private static final Identifier ID_KB = JockBall.id("set_knockback");
    private static final Identifier ID_SPD = JockBall.id("set_speed");

    private static final EquipmentSlot[] SLOTS =
            {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};

    /** Nivel efectivo del set que lleva puesto el jugador (0-5). */
    public static int effectiveLevel(Player player) {
        int min = Integer.MAX_VALUE;
        for (EquipmentSlot slot : SLOTS) {
            min = Math.min(min, ModItems.levelOf(player.getItemBySlot(slot)));
        }
        return min == Integer.MAX_VALUE ? 0 : min;
    }

    private static void apply(Player player, Holder<Attribute> attr, Identifier id, double value,
                              AttributeModifier.Operation op) {
        AttributeInstance inst = player.getAttribute(attr);
        if (inst == null) return;
        if (value == 0.0) {
            inst.removeModifier(id);
        } else {
            inst.addOrUpdateTransientModifier(new AttributeModifier(id, value, op));
        }
    }

    private static void update(ServerPlayer player, boolean feedSaturation) {
        int level = effectiveLevel(player);
        int i = level - 1;
        boolean on = level > 0;
        apply(player, Attributes.ATTACK_DAMAGE, ID_STR, on ? STRENGTH[i] : 0, AttributeModifier.Operation.ADD_VALUE);
        apply(player, Attributes.ARMOR, ID_ARM, on ? RESIST_ARMOR[i] : 0, AttributeModifier.Operation.ADD_VALUE);
        apply(player, Attributes.KNOCKBACK_RESISTANCE, ID_KB, on ? RESIST_KB[i] : 0, AttributeModifier.Operation.ADD_VALUE);
        apply(player, Attributes.MOVEMENT_SPEED, ID_SPD, on ? SPEED[i] : 0, AttributeModifier.Operation.ADD_MULTIPLIED_BASE);
        if (on && feedSaturation) {
            player.getFoodData().eat(0, SATURATION[i]);
        }
    }

    public static void initialize() {
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            int tick = server.getTickCount();
            if (tick % 10 != 0) return;
            boolean feed = tick % 40 == 0;
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                update(player, feed);
            }
        });
    }

    private SetBonus() {}
}
