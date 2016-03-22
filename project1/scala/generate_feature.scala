
// import library
import org.apache.spark._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD
import org.apache.spark.graphx.lib._

// get graph object and all indegree/outdegree/pagerank of all vertices in the graph 
val g=GraphLoader.edgeListFile(sc, "/home/printfcover/data/data/pair_set.txt", numEdgePartitions=14)
val f=g.outerJoinVertices(g.inDegrees){(_,_,y)=>y match {
case Some(d)=>d
case None =>0
}}.outerJoinVertices(g.outDegrees){(_, x,y)=> y match{
case Some(d)=>(x,d)
case None =>(x,0)
}}.mapVertices({(_,v)=>(v._1,v._2,Math.log(1.0+(1.0+v._1/(1.0+v._2))))}). outerJoinVertices(g.pageRank(1e-6).vertices){case (_, (a,b,c),y)=>y match{
case Some(d)=>(a,b,c,d)
case None =>(a,b,c,0.0)
}}
val inNeighbor=g.collectNeighborIds(EdgeDirection.In)
val outNeighbor=g.collectNeighborIds(EdgeDirection.Out)


// funciton generate_feature is used to generate node and edge features by reading edge_pair_set file 
def generate_feature(input: String, output: String, exist: Int): Unit = {
  val t=GraphLoader.edgeListFile(sc, input, numEdgePartitions=14)
  val edges=t.edges.map(e=>(e.srcId,e.dstId))
  val tmp2 = edges.join(f.vertices).map(e=>(e._2._1,(e._1,e._2._2))).join(f.vertices).map(e=>(e._2._1._1, e._1, exist, e._2._1._2, e._2._2))
  val tmp4=edges.join(inNeighbor).map(e=>(e._2._1,(e._1,e._2._2))).join(inNeighbor).map(e=>(e._2._1._1,e._1,e._2._1._2,e._2._2))
  val jacardIn=tmp4.map(e=>((e._1,e._2), if (e._3.isEmpty || e._4.isEmpty) 0.0 else {val i= e._3.intersect(e._4).size;i.toDouble/(e._3.size+e._4.size-i).toDouble}))
  val tmp5=edges.join(outNeighbor).map(e=>(e._2._1,(e._1,e._2._2))).join(outNeighbor).map(e=>(e._2._1._1,e._1,e._2._1._2,e._2._2))
  val jacardOut=tmp5.map(e=>((e._1,e._2), if (e._3.isEmpty || e._4.isEmpty) 0.0 else{val i = e._3.intersect(e._4).size;i.toDouble/(e._3.size+e._4.size-i).toDouble}))
  tmp2.map(e=>((e._1,e._2),(e._3, e._4, e._5))).join(jacardIn).join(jacardOut).saveAsTextFile(output)
}

// generate features of training set of classification 1, training set of classification 0 and test set
generate_feature("/home/printfcover/data/data/pair_set_train.txt","/home/printfcover/data/data/feature_train",1)
generate_feature("/home/printfcover/data/data/false_edges_sample.txt","/home/printfcover/data/data/feature_false",0)
generate_feature("/home/printfcover/data/data/test-public_edges.txt","/home/printfcover/data/data/feature_test",1)
