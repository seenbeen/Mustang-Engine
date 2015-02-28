from m_engine.physx import CollisionListener

class TestListener(CollisionListener):
    def onCollision(self,collision):
        V = collision.A.velocity
        if (collision.nature in ["BOTTOM","TOP"] and abs(V["y"]) > 2):
            print (collision.A.id,collision.B.id,collision.nature)
        elif (collision.nature in ["LEFT","RIGHT"] and abs(V["x"])> 2):
            print (collision.A.id,collision.B.id,collision.nature)
