public class Behavior extends Action {

    public Behavior(EntityAnimation entity, World world, ImageLibrary imageLibrary) {
        super(entity, world, imageLibrary,0);
    }

    public void execute(EventScheduler scheduler) {
        ( (EntityAnimation) getEntity()).executeBehavior(getWorld(), getImageLibrary(), scheduler);
    }
}
