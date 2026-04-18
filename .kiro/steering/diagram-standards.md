---
inclusion: fileMatch
fileMatchPattern: '.*\.(drawio|png|svg|jpg|jpeg|diagram).*'
priority: high
---

# Diagram Standards

## Core Rules
**AWS Icons**: Use Draw.io's mxgraph.aws4.* shapes  
**Orthogonal Routing**: All connectors use 90-degree angles (no diagonals)  
**No Crossovers**: Lines route around shapes, not over them  
**Labeled Flows**: All arrows labeled with step numbers + descriptions

## Connector Standards

**Required Style**:
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto
```

**Routing Pattern**:
```xml
<mxCell id="flow1" value="1. Label" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3;strokeColor=#4CAF50;" edge="1" parent="1" source="src" target="tgt">
    <mxGeometry relative="1" as="geometry">
        <Array as="points">
            <mxPoint x="300" y="200"/>
            <mxPoint x="300" y="400"/>
        </Array>
    </mxGeometry>
</mxCell>
```

## AWS Service Shapes

| Service | Shape Name |
|---------|------------|
| Lambda | `mxgraph.aws4.lambda_function` |
| API Gateway | `mxgraph.aws4.api_gateway` |
| S3 | `mxgraph.aws4.bucket` |
| DynamoDB | `mxgraph.aws4.dynamodb` |
| Neptune | `mxgraph.aws4.neptune` |
| ElastiCache | `mxgraph.aws4.elasticache` |
| OpenSearch | `mxgraph.aws4.opensearch_service` |
| Bedrock | `mxgraph.aws4.bedrock` |
| CloudWatch | `mxgraph.aws4.cloudwatch` |
| EventBridge | `mxgraph.aws4.eventbridge` |
| Step Functions | `mxgraph.aws4.step_functions` |
| VPC | `mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc` |

## Diagram Types

### Data Flow Diagrams
**Arrow Colors**:
- Primary flow: `#4CAF50` (green)
- Cache/monitoring: `#E7157B` (pink, dashed)
- AI/ML: `#01A88D` (teal)
- Database: `#8C4FFF` (purple)

**Requirements**: Performance notes, legend for arrow types

### Network Architecture
**Subnet Colors**:
- Public: `#E9F3E6` (light green)
- Private: `#E6F2F8` (light blue)
- Isolated: `#F3E5F5` (light purple)

**Requirements**: VPC grouping, AZ borders (dashed), security groups, VPC endpoints

### UML Diagrams

**MANDATORY Standards**:
- [ ] Proper UML symbology (class/state/sequence/component)
- [ ] Orthogonal routing (90-degree angles only)
- [ ] No overlapping symbols or connectors
- [ ] Consistent spacing (min 20px padding, 150-200px between elements)
- [ ] Clear labels on all relationships/transitions
- [ ] Proper stereotypes (<<interface>>, <<abstract>>, etc.)

**Relationship Arrowheads**:
| Type | Style |
|------|-------|
| Inheritance | `endArrow=block;endFill=0` (hollow triangle) |
| Realization | `endArrow=block;endFill=0;dashed=1` (hollow triangle, dashed) |
| Composition | `endArrow=diamondFill;endSize=24` (filled diamond) |
| Aggregation | `endArrow=diamond;endSize=24;endFill=0` (hollow diamond) |
| Association | `endArrow=open` (open arrow) |
| Dependency | `endArrow=open;dashed=1` (open arrow, dashed) |

**Color Coding** (optional):
- Entities: `#dae8fc` (light blue)
- Interfaces: `#e1d5ff` (light purple)
- Abstract: `#f5f5f5` (light gray)

### C4 Architecture
- Follow C4 levels (Context, Container, Component, Code)
- Consistent shapes per level
- Clear boundaries and relationships
- Technology labels

## File Organization

```
docs/3-architecture/diagrams/
├── README.md                    # Index
├── [name].drawio               # Source
├── [name].png                  # Export
```

**Export**: `draw.io -x -f png -o output.png input.drawio`

## Quality Checklist

**General**:
- [ ] Orthogonal routing (no diagonals)
- [ ] No lines over shapes
- [ ] All flows labeled with step numbers
- [ ] AWS mxgraph.aws4 shapes used
- [ ] Legend for complex diagrams
- [ ] Performance notes where relevant
- [ ] Both .drawio and .png committed
- [ ] Referenced in README.md

**UML Specific**:
- [ ] Proper UML symbology
- [ ] Orthogonal routing
- [ ] No overlapping symbols/connectors
- [ ] Consistent spacing (150-200px)
- [ ] All relationships labeled
- [ ] Proper stereotypes used
- [ ] Color coding consistent

## Programmatic Creation

### Draw.io XML Structure
```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Shapes and connectors -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### UML Class Template
```xml
<mxCell id="class1" value="ClassName&#10;--&#10;+ attr: Type&#10;--&#10;+ method(): Type" 
  style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="86" as="geometry"/>
</mxCell>
```

### UML State Template
```xml
<mxCell id="state1" value="StateName" 
  style="rounded=1;whiteSpace=wrap;html=1;strokeWidth=2;fillColor=#dae8fc;strokeColor=#6c8ebf;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="60" as="geometry"/>
</mxCell>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Icons show as boxes | Verify `shape=mxgraph.aws4.[service]`, check AWS library loaded |
| Lines cross shapes | Add waypoints with `<Array as="points">` |
| Diagonal lines | Ensure `edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1` |
| Symbols overlap | Increase spacing (150-200px), use grid alignment |
| Connectors cross | Add waypoints, use vertical-then-horizontal routing |

## References
- Draw.io AWS: https://www.drawio.com/blog/aws-diagrams
- AWS Icons: `ALM-SSDLC-Library/assets/AWS/`
- UML Spec: https://www.omg.org/spec/UML/
- Examples: `Nagara-Chishiki/docs/3-architecture/diagrams/`, `docs/4-design/diagrams/`

---

**Status**: Active | **Updated**: 2025-11-24
