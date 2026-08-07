package com.here.gluecodium.generator.python

import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.generator.common.nameRuleSetFromConfig
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributes
import com.here.gluecodium.model.lime.LimeDirectTypeRef
import com.here.gluecodium.model.lime.LimePath
import com.here.gluecodium.model.lime.LimeStruct
import com.natpryce.konfig.ConfigurationProperties
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.runners.JUnit4
import java.util.logging.Logger

@RunWith(JUnit4::class)
class PythonNameResolverTest {
    @Test
    fun `resolves direct reference to retained duplicate type`() {
        val publicType = LimeStruct(LimePath(listOf("sdk", "routing"), listOf("TbtManeuver"), "public"))
        val internalType =
            LimeStruct(
                LimePath(listOf("sdk", "routing"), listOf("TbtManeuver"), "internal"),
                attributes = LimeAttributes.Builder()
                    .addAttribute(LimeAttributeType.INTERNAL)
                    .build(),
            )
        val referenceMap = mapOf(internalType.path.toAmbiguousString() to internalType)
        val resolver =
            PythonNameResolver(
                referenceMap,
                PythonNameRules(
                    nameRuleSetFromConfig(
                        ConfigurationProperties.fromResource(javaClass, "/namerules/python.properties"),
                    ),
                ),
                LimeLogger(Logger.getAnonymousLogger(), emptyMap()),
                PythonCommentsProcessor(false),
            )

        assertEquals("_TbtManeuver", resolver.resolveName(LimeDirectTypeRef(publicType)))
    }
}
